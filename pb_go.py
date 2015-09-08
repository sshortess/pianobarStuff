#!/usr/bin/env python


import psutil
import subprocess as subp
import shlex
import socket
import threading
import time
import Queue


import pianobar_cmds as pb_cmds


"""
   launch pianobar in separate window
   launch command processor server in thread

   wait for pianobar exit
   tell server to end
   wait for server

   done
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class s_exception(Exception):
   """
   """
   pass

def sig_handle(signum, frame):
   """
      signal handler
   """
   raise s_exception
   

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def launch_pianoBar():
   process = subp.Popen(shlex.split("""lxterminal -e 'bash -c "pianobar"'"""),stdout=subp.PIPE)

   process.wait()
   
   return 'pianobar'


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def find_proc(proc_name):
   """
      find a process with name
      return dict with pid,name
   """

   for proc in psutil.process_iter():
      try:
         pinfo = proc.as_dict(attrs=['pid','name'])
      except psutil.NoSuchProcess:
         pass
      else:
         # print pinfo
         if proc_name.find(pinfo['name']) >=0:
            print 'found it'
            print pinfo
            return pinfo

   return None         

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def check_proc(proc_pid):
   """
   """
   if psutil.pid_exists(proc_pid):
      return True
   else:
      return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def watch_process(proc_pid, w_event):
   """
   """
   print "Watching pianobar"
   try:
      while psutil.pid_exists(proc_pid) and w_event.is_set():
         #print "Watching pianobar"
         time.sleep(1)
         pass
      else:
         w_event.clear()
   except:
      pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def cmd_processor(c_event,c_queue):
   """
   """
   try:
      while c_event.is_set():
         while not c_queue.empty():
            cmd = c_queue.get()
            pb_cmds.pb_cmd_processor(cmd) 
   except:
      pass


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def launch_cmd_server(s_event, s_queue, HOST='', PORT=5008):
   """
   """
   
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   print 'socket created'

   # bind the socket to port
   try:
      s.bind((HOST,PORT))
   except socket.error as msg:
      print 'Bind failed. Error Code: %d, Message: %s' % (msg[0], msg[1])  
      return
   
   print 'bind complete'

   #set timeout
   s.settimeout(5.0)

   #start listening
   s.listen(10)
   print 'listening'

   while s_event.is_set():
      try:
         #wait for data
         conn, addr = s.accept()
         print 'info from %s: %d' % (addr[0], addr[1])

         while s_event.is_set():
            data = conn.recv(1024)
            if not data:
               break
            print data
            s_queue.put(data)
            conn.sendall('ok')

      except socket.timeout:
         pass
      except:
         s.close()
         s_event.clear()
         break
   else:
      s.close()
      s_event.clear()

   print ' '

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def pianoBar_go():
   """
   """

   # launch pianobar player
   proc_name = 'pianobar' #plug in for now
   proc_info = find_proc(proc_name)
   if not proc_info:
      proc_name = launch_pianoBar()
      for i in xrange(5):
         proc_info = find_proc(proc_name)
         if proc_info:
            break
         time.sleep(1)
   else:
      print "pianobar not started"
      return None

   # setup event and queue
   s_event = threading.Event()
   s_event.set()
   s_queue = Queue.Queue()

   # start the command processot thread
   t_cmd = threading.Thread(target = cmd_processor, args = ( s_event, s_queue ))
   t_cmd.start()
   
   # start the 'watcher' thread
   proc_pid = proc_info['pid']
   t_watch = threading.Thread(target = watch_process, args = (proc_pid, s_event))
   t_watch.start()

   # launch the server
   launch_cmd_server(s_event, s_queue)
   #t_server= threading.Thread(target = launch_cmd_server, args = (s_event, s_queue))
   #t_server.start()
   #t_server.join()



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=="__main__":

   pianoBar_go()




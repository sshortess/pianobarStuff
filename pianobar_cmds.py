#!/usr/bin/env python

"""
   pianobar command thingie
"""

import os
import sys
import socket
import threading
import time

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pb_commands = {'n':('n','next song'), 'next':('n','next song'),
      'p':('p','pause/resume toggle'),'P':('P','play/resume'),
      'S':('S','pause'), 'pause':('S','pause'),
      '+':('+','love the song'), 'love':('+','love the song'),
      '-':('-','ban this song'), 'ban':('-','ban this song'),
      '(':('(','louder'), 'louder':('(','louder'),
      ')':(')','softer'), 'softer':(')','softer'),
      '?':('?','help'), 'help':('?','help'),
      'q':('q','quit'), 'quit':('q','quit')}


def pb_send_cmd(cmd):
   """
   """
   with open('/home/steve/.config/pianobar/ctl','w') as fp:
     fp.write(cmd)

def pb_find_cmd(s_cmd):
   """
   """
   try:
      t_cmd = pb_commands[s_cmd]
      return t_cmd[0]
   except KeyError:
      return '?'

def pb_cmd_processor(cmd_line):
   """
      process commands
   """

   if len(cmd_line) > 0:
      s_cmd = cmd_line[0]
      cmd = pb_find_cmd(s_cmd)
      print cmd
      # pb_send_cmd(cmd)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def simple_server(HOST='', PORT=5008):
   """
   """
   
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   print 'socket created'

   # bind the socket to port
   try:
      s.bind((HOST,PORT))
   except socket.error as msg:
      print 'Bind failed. Error Code: %d, Message: %s' % (msg[0], msg[1])  
      sys.exit()
   
   print 'bind complete'

   #start listening
   s.listen(10)
   print 'listening'

   try:
      while 1:
         #wait for data
         conn, addr = s.accept()
         print 'info from %s: %d' % (addr[0], addr[1])

         while True:
            data = conn.recv(1024)
            if not data:
               break
            print data
            pb_cmd_processor(data)
            conn.sendall('ok')
   except:
      s.close()

   s.close()
   print ' '

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":
   
   # parse command line/options
   if len(sys.argv) > 1:
      pb_cmd_processor(sys.argv[1:])
   else:
      simple_server()




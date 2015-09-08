#!/usr/bin/env python

"""
   pianobar command client
"""


import socket
import sys


def snd_cmd(cmd):
   """
   """
   #HOST = socket.gethostname()
   HOST = socket.gethostbyname('ruth')
   PORT = 5008

   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   print 'socket created'

   try:
      s.connect((HOST,PORT))
      #s.sendall(b'p')
      s.sendall(cmd)
      data = s.recv(1024)
      print data
      """
      s.sendall(b'help')
      data = s.recv(1024)
      print data
      s.sendall(b'pause')
      data = s.recv(1024)
      print data
      s.sendall(b'S')
      data = s.recv(1024)
      print data
      s.sendall(b'next')
      data = s.recv(1024)
      print data
      """
   except:
      pass

   s.close()



if __name__ == "__main__":

   if len(sys.argv) >1:
      snd_cmd(sys.argv[1])
   else:
      snd_cmd('p')





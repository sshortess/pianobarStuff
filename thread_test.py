#!/usr/bin/env python

import os
import sys
import threading
import time



"""
   launch a thread
   wait for event clear
   end
"""

def the_thread(t_event):
   """
   """

   counter = 0
   print "start thread"

   while t_event.is_set():
      print "waiting"
      time.sleep(5)
      counter = counter +1
      if counter >5:
         sys.exit()


if __name__ == "__main__":

   t_event = threading.Event()
   t_event.set()

   t = threading.Thread(target=the_thread, args=(t_event,))
   t.start()

   while t_event.is_set():
      try:
         print "main loop"
         time.sleep(2)
      except :
         t_event.clear()
         t.join()



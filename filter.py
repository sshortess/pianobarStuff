#!/usr/bin/env python

import fileinput


fh_out = open("pb.out.filt","w")
for line in fileinput.input("pb.out.tmp"):
   p2 = line.rfind('\r')
   if p2 >=0:
      p2 +=1
      l2 = line[p2:]
   else:
      l2 = line

   if l2.startswith("\x1b"):
      l3 = l2[4:]
   else:
      l3 = l2

   print l3
   fh_out.write(l3)


fh_out.close()


#!/usr/bin/python
import sys
import commands
import os
if len(sys.argv) <> 4:
	print "Usage: " + sys.argv[0] + " file1 file2"
	sys.exit(-1)
file1=open(sys.argv[1],'r')
file2=open(sys.argv[2],'r')
file3=open(sys.argv[3],'w')
file1_dict={}
Line1=file1.readlines()
for line1 in Line1:
	lin1=line1.split('\t')
	file1_dict[lin1[1]]=lin1[0]
Line2=file2.readlines()
for line2 in Line2:
	lin2=line2.split('\t')
	group=file1_dict[lin2[0]]
	file3.write(group+'\t'+'\t'.join(lin2[1:]))
file1.close()
file2.close()
file3.close()

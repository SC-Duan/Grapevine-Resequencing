#!/usr/bin/python
import sys
import commands
import os
import math
import numpy as np
if len(sys.argv) <> 5:
	print "Usage: " + sys.argv[0] + " input output_signification output_to_plot signification_cutoff (0.05)"
	sys.exit(-1)
file1=open(sys.argv[1],'r')
file2=open(sys.argv[2],'w')
file3=open(sys.argv[3],'w')
top=float(sys.argv[4])
file2.write('Chr\tBin_start\tBin_end\tFst\tPi_log2\n')
file3.write('Fst\tPi_log2\n')
head=file1.readline()
fst_list=[]
pi_list=[]
Line1=file1.readlines()
for line1 in Line1:
	lin1=line1.strip('\n').split('\t')
	fst_list.append(float(lin1[3]))
	if float(lin1[4])==0 or float(lin1[5])==0:
		pi_list.append(float(0))
	else:
		pi=np.log2(float(lin1[4])/float(lin1[5]))
		pi_list.append(float(pi))
#	file2.write('\t'.join(lin1[:4])+'\t'+str(pi)+'\n')
fst_list_sorted=sorted(fst_list,reverse=True)
fst_index=int(math.ceil(float(len(fst_list))*top))
fst_cut_off=fst_list_sorted[fst_index]
pi_list_sorted=sorted(pi_list,reverse=True)
pi_index=int(math.ceil(float(len(pi_list))*top))
pi_cut_off=pi_list_sorted[pi_index]
file_name=sys.argv[1]+'.threshold.txt'
file=open(file_name,'w')
file.write('Fst_cutoff\tPi_cutoff\n')
file.write(str(fst_cut_off)+'\t'+str(pi_cut_off)+'\n')
file.close()
for line1 in Line1:
	lin1=line1.strip('\n').split('\t')
	if float(lin1[4]) !=0 and float(lin1[5]) !=0:
		pi=np.log2(float(lin1[4])/float(lin1[5]))
		if float(lin1[3]) > fst_cut_off and float(pi) > pi_cut_off:
			file2.write('\t'.join(lin1[:4])+'\t'+str(pi)+'\n')
for i in range(0,len(fst_list)):
	file3.write(str(fst_list[i])+'\t'+str(pi_list[i])+'\n')
file1.close()
file2.close()
file3.close()

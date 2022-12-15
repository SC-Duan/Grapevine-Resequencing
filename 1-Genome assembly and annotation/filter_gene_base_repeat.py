#!/usr/bin/python
import sys
import commands
import os
import random
import math
if len(sys.argv) <> 6:
        print "Usage: " + sys.argv[0] + " gene_bed repeat_bed out_all out_filtered set_repeat_percent(0.5) \nwrited by dsc"
        sys.exit(-1)
file1=open(sys.argv[1],'r')
file2=open(sys.argv[2],'r')
file3=open(sys.argv[3],'w')
file4=open(sys.argv[4],'w')
set_repeat_percent=float(sys.argv[5])
file3.write('Chr\tStart\tEnd\tStrand\tGene\tRepeat_Percent\n')
file4.write('Chr\tStart\tEnd\tStrand\tGene\tRepeat_Percent\n')
Line1=file1.readlines()
Line2=file2.readlines()
for line1 in Line1:
	lin1=line1.strip('\n').split('\t')
	gene_length=int(int(lin1[2])-int(lin1[1])+1)
	repeat_length=0
	for line2 in Line2:
		lin2=line2.strip('\n').split('\t')
		if lin2[3]==lin1[3]:
			if lin2[0]==lin1[0]:
				if int(lin2[2]) < int(lin1[1]):
					continue
				else:
					if int(lin2[1])>int(lin1[2]):
						break
					else:
						if int(lin2[1])<=int(lin1[1]) and int(lin2[2])>=int(lin1[2]): #repeat cover
							repeat_length=int(int(lin1[2])-int(lin1[1])+1)
							break
						else:
							if int(lin2[1])<=int(lin1[1]) and int(lin2[2])>int(lin1[1]) and int(lin2[2])<=int(lin1[2]): #left overlap
								repeat_length+=int(int(lin2[2])-int(lin1[1])+1)
							else:
								if int(lin2[1])>=int(lin1[1]) and int(lin2[2])<=int(lin1[2]): #cover repeat
									repeat_length+=int(int(lin2[2])-int(lin2[1])+1)
                                        			else:
                                                			if int(lin2[1])>=int(lin1[1]) and int(lin2[1])<int(lin1[2]) and int(lin2[2])>int(lin1[2]): #right overlap
										repeat_length+=int(int(lin1[2])-int(lin2[1])+1)
										break
	repeat_percent='%.3f' % float(float(repeat_length)/float(gene_length))
	file3.write('\t'.join(lin1)+'\t'+str(repeat_percent)+'\n')
	if float(set_repeat_percent) == 0:
		if float(repeat_percent) == 0:
			file4.write('\t'.join(lin1)+'\t'+str(repeat_percent)+'\n')
	else:
		if float(repeat_percent) < float(set_repeat_percent):
			file4.write('\t'.join(lin1)+'\t'+str(repeat_percent)+'\n')
file1.close()
file2.close()
file3.close()
file4.close()

#!/usr/bin/python
import sys
import commands
import os
import random
import math
if len(sys.argv) <> 6:
        print "Usage: " + sys.argv[0] + " gff3 all_out filtered_out set_CDS_lengt(300) set_exon_nuber(0) \nwrited by dsc"
        sys.exit(-1)
file1=open(sys.argv[1],'r')
file2=open(sys.argv[2],'w')
file3=open(sys.argv[3],'w')
set_CDS_lengt=sys.argv[4]
set_exon_nuber=sys.argv[5]
file2.write('Gene\texon_number\tCDS_length\n')
file3.write('Gene\texon_number\tCDS_length\n')
new_file=[]
Line=file1.readlines()
for line in Line:
	if len(line)>1:
		if '#' not in line:
			new_file.append(line)
line1=new_file[0]
lin1=line1.split('\t')
exon_num=0
cds_len=0
for i in range(1,len(new_file)):
	line2=new_file[i]
	lin2=line2.split('\t')
	if lin2[2]=='CDS':
		exon_num+=1
		length=int(int(lin2[4])-int(lin2[3])+1)
		cds_len+=length
	else:
		if lin2[2]=='gene':
			file2.write(lin1[8].split(';')[0].split('=')[1]+'\t'+str(exon_num)+'\t'+str(cds_len)+'\n')
			if int(exon_num) > int(set_exon_nuber) and int(cds_len)>=int(set_CDS_lengt):
				file3.write(lin1[8].split(';')[0].split('=')[1]+'\t'+str(exon_num)+'\t'+str(cds_len)+'\n')
			line1=line2
			lin1=lin2
			exon_num=0
			cds_len=0
file2.write(lin1[8].split(';')[0].split('=')[1]+'\t'+str(exon_num)+'\t'+str(cds_len)+'\n')
if int(exon_num) >int(set_exon_nuber) and int(cds_len)>=int(set_CDS_lengt):
	file3.write(lin1[8].split(';')[0].split('=')[1]+'\t'+str(exon_num)+'\t'+str(cds_len)+'\n') #last line
file1.close()
file2.close()
file3.close()

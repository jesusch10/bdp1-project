#!/usr/bin/python
import sys
import os
from timeit import default_timer as timer

start = timer()
dbpath = "/data2/BDP1_2022/hg19/"
dbname = "hg19bwaidx"
queryname = sys.argv[1]
out_name = queryname[:-3]
md5file = "md5.txt"

command = "/data2/BDP1_2022/condor/hg/bwa aln -t 1 " + dbpath + dbname + " " + queryname + " > " + out_name + ".sai "
print("Launching command: " + command)
os.system(command)

command = "/data2/BDP1_2022/condor/hg/bwa samse -n 10 " + dbpath + dbname + " " + out_name + ".sai " + queryname + " > " + out_name + ".sam "
print("Launching command: " + command)
os.system(command)

print("Creating md5sums")
os.system("md5sum " + out_name + ".sai" + " > " + md5file)
os. system("md5sum " + out_name + ".sam" + " >> " + md5file)

print("gzipping out text file")
command = " gzip " + out_name + ".sam "

print("Launching command: " + command)
os.system(command)

execution_time = timer() - start
print("Total execution time: " + str(execution_time))
print("Exiting")
exit(0)

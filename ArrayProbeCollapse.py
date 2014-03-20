import os, sys

finpath = sys.argv[1]
foutpath = sys.argv[2]
mode = sys.argv[3]

if False == os.path.exist(finpath):
    print "\n. I can't find your input file", finpath

fin = open(finpath, "r")
for l in 

    
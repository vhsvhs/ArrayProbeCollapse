##################################################################################
#
# ArrayProbeCollapse.py
#
# written by Victor Hanson-Smith
# victorhansonsmith@gmail.com
#
# This Python script reads microarray data and then collapses redundant probe
# reads by calculating their mean, or median.
#
##################################################################################
# USAGE: Invoke this script from the Terminal or command-line
#
# %> python ArrayProbeCollapse.py INPATH OUTPATH MODE
#
# INPATH is the filepath to your uncollapsed original data. This
# file must have a header row.
#
# OUTPATH is the filepath to your desired output file. This file
# will be created new, or overwritten if it already exists.
#
# MODE indicates if collapsing should occur by averaging, or by taking
# the median. For the average, specify F or mean. For the median,
# specify T or median.
#
# EXAMPLE:
# %> python ArrayProbeCollapse.py mydata.txt mydata.median.out.txt median
#
# . . . will read the file mydata.txt, collapse redundant rows by taking the median,
# and then write the results to mydata.median.out.txt
#
# %> python ArrayProbeCollapse.py mydata.txt mydata.mean.out.txt F
#
# . . . will read the file mydata.txt, collapse redundant rows by taking the mean,
# and then write the results to mydata.mean.out.txt
#
#######################################################################################

import os, sys

def usage():
    print "\n\nArrayProbeCollapse.py"
    print ""
    print "Usage:"
    print "$> python ArrayProbeCollapse.py INPATH OUTPATH MODE"
    print ""
    print "INPATH is the path to your input file."
    print "OUTPUT is the desired path to your (collapsed) output file."
    print "MODE is approach to collapsing, either 'mean' or 'median'."
    print "\n"

if sys.argv.__len__() < 4:
    print "\n\n\n---> Ooops, you didn't specify enough arguments."
    usage()
    exit()

finpath = sys.argv[1] # the input path
foutpath = sys.argv[2] # the output path
mode = sys.argv[3] # the mode (mean or median)
if False == os.path.exists(finpath):
    print "\n. I can't find your input file", finpath
if mode != "mean" and mode != "median" and mode != "F" and mode != "T":
    print "\n. The third argument should be either 'mean' or 'median'"
    usage()
    exit()

def mean(set):
    if set.__len__() == 0:
        return None
    sum = 0.0
    for x in set:
        sum += x
    return sum / float( set.__len__() )

def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
    return sorts[length / 2]

def read_input(finpath):
    name_data = {} # key = name of row, value = array of arrays
    header_line = []
    
    fin = open(finpath, "r")
    firstline = True
    countlines = 0
    for l in fin.xreadlines():
        # Skip empty lines:
        if l.__len__() < 2:
            continue
        # Skip the header row:
        if firstline:
            firstline = False
            header_line = l
        else:
            countlines += 1
            tokens = l.split()
            name = tokens[0]
            if name not in name_data:
                name_data[name] = []
                for ii in range(1, tokens.__len__()):
                    name_data[name].append([])
            
            floattokens = []
            for ii in range(1, tokens.__len__()):
                try:
                    value = float(tokens[ii])
                    name_data[name][ii-1].append( value )
                except ValueError:
                    pass
    print "\n. OK, I found", name_data.keys().__len__(), "unique probe names, and",countlines,"total rows of data."                   
    return [name_data, header_line]

def collapse(name_data):
    if mode == "mean" or mode == "F": 
        print "\n. I'm collapsing redundant probes by computing their mean."
    if mode == "median" or mode == "T": 
        print "\n. I'm collapsing redundant probes by computing their median."
    
    collapsed_data = {}
    for name in name_data:
        collapsed_data[name] = []
        for col in range(0, name_data[name].__len__()):
            if name_data[name][col].__len__() < 1:
                collapsed_data[name].append( "NA" )
            else:
                if mode == "mean" or mode == "F":                
                    collapsed_data[name].append( "%.3f"%mean(name_data[name][col]) )
                elif mode == "median" or mode == "T":                
                    collapsed_data[name].append( "%.3f"%median(name_data[name][col]) )
    return collapsed_data

def write_output(name_data, header):
    print "\n. I'm writing the collapsed data to", foutpath
    fout = open(foutpath, "w")
    names = name_data.keys()
    names.sort()
    
    fout.write(header + "\n") 
    
    for name in names:
        fout.write(name + "\t")
        fout.write( "\t".join( name_data[name] ) + "\n" )
    fout.close()

#######################################
#
# Main:
#
[name_data, header] = read_input(finpath)
collapsed_name_data = collapse(name_data)
write_output(collapsed_name_data, header)
print "\n. I'm done. Goodbye.\n"


    
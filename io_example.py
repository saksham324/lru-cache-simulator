#io.py
#
#Tucker L. Ward
#tucker.l.ward.12@dartmouth.edu
#
#created May 2013
#
#A simple program to demonstrate file I/O in Python. Reads in a file
#consisting of a single character, a space, and a 32-bit address in hex.
#File is specified as command-line argument; if argument is '-' reads from
#stdin
#
#CAUTION: minimal checking. onus is on user to provide a properly-formatted
#file...or add those checks yourself.
#
#USAGE: call main with argument of the target filename. or, if stdin is desired,
#call main with argument '-' or "-". exits automatically with file read option;
#to exit from stdin, just type exit

# Edited by Saksham Arora 
# saksham.arora.23@dartmouth.edu 
# May 2022 

#for stdin
import sys

def main(filename):
    
    #stdin or a file?
    if (filename == '-'):
        in_file = sys.stdin
    else:
        try:#ensure the file exists
            with open(filename, "r"):
                in_file = open(filename, "r")
        except IOError: #throw exception if it does not
            print("ERROR: file \"" + filename + "\" does not exist")
            return

    list_addresses = []
    
    #read in each line of the file
    line = in_file.readline()
    while line:
        
        #strip line
        stripped_line = line.strip()
        
        #should I exit?
        if ( stripped_line == "exit" ):
            if (filename != '-'):
                in_file.close()
            return

        #process line into its components
        args = stripped_line.split(" ")
        
        #assign instr/data and the address
        c = args[0] #holds D or I
        n = int(args[1], 16) #holds an unsigned int of the address (at least 32 bits)
        
        # #print the result
        # if c == 'I':
        #     # print("instruction fetch, address: 0x" + args[1]) #NOTE: n holds the int, not args[1]!!
        #     list_addresses.append(n)
        # elif c == 'D':
        #     # print("data, address: " + args[1]) #NOTE: n holds the int, not args[1]!!
        #     list_addresses.append(n)
        # # else:
        # #     print("??")

        list_addresses.append(n)


        line = in_file.readline()
        
    #close the input file
    in_file.close()
    return list_addresses
    
# list_addresses = main("/Users/sakshamarora/cs51/hw7/Q1/long-trace.txt")
# textfile = open("a_file.txt", "w")
# for element in list_addresses:
#     print(element)
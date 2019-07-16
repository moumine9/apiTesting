#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import getopt
from yaml import load
from helpers import *

def main(argv):

    inputfile = ""
    outputfile = ""
    verbose = True
    auth = {'method':'none', 'params':'none'}

    try:
        opts, args = getopt.getopt(argv,"hi:o:v:a:k:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        if opt in ("-i", "--ifile"):
            inputfile = arg
        if opt in ("-o", "--ofile"):
            outputfile = arg
        if opt == "-v":
            verbose = False
        if opt == "-a":
            auth["method"] = arg
        if opt == "-k":
            auth["params"] = arg
        
    if(auth["method"] != "none" and auth["params"] == "none"):
            print("Authentication params are missing")
            print("Ex : apiTesting.py -a AuhMethod -k AuthParams")
            sys.exit(2)
            


    if( inputfile != "" ):
        stream = open(inputfile, 'r')
        if( 'json' in inputfile):
            tests_data = json.load(stream)
        if('yaml' in inputfile):
            tests_data = load(stream)
        tests_info = { "name" : tests_data["name"], "base_url": tests_data["base_url"] }
        
        tests_results = execute_tests(tests_data, auth)

        if(verbose):
            display_log(tests_results)

        if(outputfile != ""):
            if (export_results(outputfile, tests_info, tests_results)):
                print("Report has been exported in <%s> \n" % outputfile)
            else:
                print("Format is not supported. Types supported are .html,.csv,.json.,.yaml \n")
    
    else:
        print("Input file is not specified.")
    

if __name__ == "__main__":
   main(sys.argv[1:])

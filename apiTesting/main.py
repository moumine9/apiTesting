#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import getopt
import requests
from yaml import load
from helpers import *

def main(argv):

    inputfile = "tests.yaml"
    outputfile = ""
    verbose = True

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt == "-v":
            verbose = False


    stream = open(inputfile, 'r')
    tests_data = load(stream)
    tests_info = { "name" : tests_data["name"], "base_url": tests_data["base_url"] }
    
    tests_results = execute_tests(tests_data)

    if(verbose):
        display_log(tests_results)

    if(outputfile != ""):
        if (export_results(outputfile, tests_info, tests_results)):
            print("Report has been exported in <%s> \n" % outputfile)
        else:
            print("Format is not supported. Types supported are .html,.csv,.json.,.yaml \n")
    

if __name__ == "__main__":
   main(sys.argv[1:])
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
    outputfile = "results.html"
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
    tests_results = []

    for test in tests_data["test_cases"]:

        if ( (test['method'] == 'POST' or test['method'] == 'PUT' or test['method'] == 'UPDATE' or test['method'] == 'PATCH') and ('data' not in test) ):
            raise ValueError("No post data provided")
        
        start = now() #variable to record request start time.
        complete_url = check_url( tests_data["base_url"], test["url"] )

        if(test['method'] == 'POST'):
            req = requests.post( complete_url , data = test['data'] )

        if(test['method'] == 'PUT'):
            req = requests.put( complete_url , data = test['data'])

        if(test['method'] == 'HEAD'):
            req = requests.head( complete_url , data = json.dumps(test['data']) )

        if(test['method'] == 'GET'):
            req = requests.get( complete_url )
        
        tests_results.insert(-1,clean_response(req, test, ( now() - start ) ))

    for test in tests_results:
        res = "N/A"
        status_code = test['result']['status_code']
        body = test['result']['body']

        if( (status_code == body == "OK") or (status_code == body == "N/A")  ):
            res = "OK"
        elif( status_code == "OK" and body == "N/A" ):
            res = "OK"
        elif( status_code == "N/A" and body == "OK" ):
            res = "OK"
        else:
            res = "FAILED"

        print("Test : %s | %s | %s" % (test["name"], test["method"], res ) )


    page = generate_body(tests_info,tests_results)

    output = open(outputfile,'w')
    output.write(page)

if __name__ == "__main__":
   main(sys.argv[1:])
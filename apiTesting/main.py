#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import yaml
from yaml import load, dump
from helpers import *

stream = open('tests.yaml', 'r')
tests_data = load(stream)
tests_info = { "name" : tests_data["name"], "base_url": tests_data["base_url"] }
tests_results = []

for test in tests_data["test_cases"]:
    if ( (test['method'] == 'POST' or test['method'] == 'PUT' or test['method'] == 'UPDATE' or test['method'] == 'PATCH') and ('data' not in test) ):
        raise ValueError("No post data provided")
    
    if(test['method'] == 'POST'):
        req = requests.post(tests_data['base_url'] + test['url'], data = test['data'])
        tests_results.insert(-1,clean_response(req, test))

    if(test['method'] == 'PUT'):
        req = requests.put(tests_data['base_url'] + test['url'], data = test['data'])
        tests_results.insert(-1,clean_response(req, test))

    if(test['method'] == 'HEAD'):
        req = requests.head(tests_data['base_url'] + test['url'], data = json.dumps(test['data']) )
        tests_results.insert(-1,clean_response(req, test))

    if(test['method'] == 'GET'):
        req = requests.get(tests_data['base_url'] + test['url'])
        tests_results.insert(-1, clean_response(req, test) )

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

    print("Test : %s | %s | %s" % (test["name"], test["method"], res) )


page = generate_body(tests_info,tests_results)

output = open('results.html','w')
output.write(page)
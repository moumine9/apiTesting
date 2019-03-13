#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import yaml
from yaml import load, dump
from helpers import *

stream = open('tests.yaml', 'r')
tests_data = load(stream)
tests_results = []

for test in tests_data["test_cases"]:
    print("Test : %s | %s " % (test["name"], test["method"]) )
    if ( (test['method'] == 'POST' or test['method'] == 'PUT' or test['method'] == 'UPDATE' or test['method'] == 'PATCH') and ('data' not in test) ):
        raise ValueError("No post data provided")
    
    if(test['method'] == 'POST'):
        req = requests.post(tests_data['base_url'] + test['url'], data = test['data'])
        tests_results.insert(-1,clean_response(req, test))

    if(test['method'] == 'PUT'):
        req = requests.put(tests_data['base_url'] + test['url'], data = test['data'])
        tests_results.insert(-1,clean_response(req, test))

    if(test['method'] == 'HEAD'):
        req = requests.head(tests_data['base_url'] + test['url'], data = test['data'])
        tests_results.insert(-1,clean_response(req, test))

    if(test['method'] == 'GET'):
        req = requests.get(tests_data['base_url'] + test['url'])
        tests_results.insert(-1, clean_response(req, test) )

print(tests_results)
generate_body(tests_results)
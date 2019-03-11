#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import yaml
from yaml import load, dump

#r = requests.get('https://api.github.com', auth=('user', 'pass'))

def clean_response(response, test):
    req = ()

    req["url"] = test["url"]
    req["name"] = test["name"]
    req["result"] = ()
    req["result"]["stat"] = ("OK", "FAILED")[response.status_code == int(test['response']['status_code']) ]
    req["result"]["body"] = test["res"]

    return req

stream = open('tests.yaml', 'r')
tests_data = load(stream)
tests_results = ()

for test in tests_data["test_cases"]:
    print("Test : %s | %s " % (test["name"], test["method"]) )
    if ( (test['method'] == 'POST' || test['method'] == 'PUT' || test['method'] == 'UPDATE' || test['method'] == 'PATCH') && 'data' not in test:
        raise ValueError("No post data provided"))
    
    if(test['method'] == 'POST'):
        req = requests.post(tests_data['base_url'] + test['url'], data = test['data'])
        tests.results[] = clean_response(req.json(), test)

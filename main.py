#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import yaml
from yaml import load, dump
import helpers

stream = open('tests.yaml', 'r')
tests_data = load(stream)
tests_results = ()

for test in tests_data["test_cases"]:
    print("Test : %s | %s " % (test["name"], test["method"]) )
    if ( (test['method'] == 'POST' OR test['method'] == 'PUT' OR test['method'] == 'UPDATE' OR test['method'] == 'PATCH') AND 'data' not in test:
        raise ValueError("No post data provided"))
    
    if(test['method'] == 'POST'):
        req = requests.post(tests_data['base_url'] + test['url'], data = test['data'])
        tests.results[] = clean_response(req.json(), test)

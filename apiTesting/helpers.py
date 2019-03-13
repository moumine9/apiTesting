#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import faker


# Function for taking the response and returning a proper array.
def clean_response(response, test):
    req = {}
    
    req["url"] = test["url"]
    req["name"] = test["name"]
    req["result"] = {}
    req["result"]["stat"] = ("OK", "FAILED")[response.status_code == int(test['response']['status_code']) ]

    return req

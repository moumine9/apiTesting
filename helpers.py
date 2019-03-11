#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import faker

# Function for replacing values in JSON to random values.
def json_formatting(json_raw):
    json_string = json.dumps(json_raw)

    #Replacing variable by their content


    return json.parse(json_string)

# Function for taking the response and returning a proper array.
def clean_response(response, test):
    req = ()

    req["url"] = test["url"]
    req["name"] = test["name"]
    req["result"] = ()
    req["result"]["stat"] = ("OK", "FAILED")[response.status_code == int(test['response']['status_code']) ]
    req["result"]["body"] = test["res"]

    return req

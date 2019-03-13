#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import faker
from htmlBuilder.tags import *
from htmlBuilder.attributes import Class, InlineStyle
from yattag import Doc

from jinja2 import Template

page = """




"""

# Function for taking the response and returning a proper array.
def clean_response(response, test):
    req = {}
    
    req["url"] = test["url"]
    req["name"] = test["name"]
    req["result"] = {"status_code":"N/A", "body":"N/A"}
    req["result"]["stat"] = ("FAILED", "OK")[response.status_code == int(test['response']['status_code']) ]
    
    if( 'status_code' in test['response'] ):
        req['result']['status_code'] = ("FAILED", "OK")[ int(response.status_code) == int(test['response']['status_code']) ]
    
    if( 'body' in test['response'] ):
        req['result']['body'] = ("FAILED", "OK")[ json.dumps(response.json()) == json.dumps(test['response']['body']) ]
    
    return req


#Function to build the html page
def generate_body(results):
    doc, tag, text = Doc().tagtext()

    with tag('html'):
        with tag('head'):
            with tag('link')

    print(doc.getvalue())  
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import faker
import datetime
from datetime import timedelta
from jinja2 import Template

page = """

<!doctype html>
<html class="no-js" lang="">

<head>
  <meta charset="utf-8">
  <title>API Tests Results</title>
  <meta name="description" content="">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
  <link rel="stylesheet" href="https://bootswatch.com/4/litera/bootstrap.min.css">

</head>

<body>
  <!--[if IE]>
    <p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>
  <![endif]-->

  <style>
  body{margin-top:5%; margin-bottom:5%;}
  table{margin:5%;}
  </style>

  <div class="container">

    <h1 class='text-center'>{{ test_name }}</h1>
    <p class='text-center text-muted'>{{ test_url }}</p>

    <table class="table table-hover table-striped table-bordered col-10">

        <thead>

            <tr class="table-dark">
                <th scope="col">Name</th>
                <th scope="col">Url</th>
                <th scope="col" class="text-center">Method</th>
                <th scope="col" class="text-center">Results</th>
                <th scope="col" class="text-center">Time</th>
            </tr>

        </thead>

        <tbody>

        {% for test in tests %}

            <tr>
                <th> {{ test.name }} </th>
                <th> {{ test.url }} </th>
                <td class="text-center"> {{ test.method }} </td>
                <td class="text-center">

                    {% if test.result.status_code == 'FAILED' or test.result.body == 'FAILED' %}
                        <i class="fas fa-circle text-danger fa-md"></i>
                    {% else %}
                        <i class="fas fa-circle text-success fa-md"></i>
                    {%- endif %}
                </td>
                <td class="text-center"> {{ test.time }} </td>
            </tr>

        {% endfor %}

        </tbody>

    </table> 

    </div>

</body>

</html>

"""

# Function for taking the response and returning a proper array.
def clean_response(response, test, delay):
    req = {}

    req["url"] = test["url"]
    req["name"] = test["name"]
    req["method"] = test['method']
    req["result"] = {"status_code":"N/A", "body":"N/A"}
    req["time"] = "{:.2f}".format( (delay.microseconds)/1000 ) + " ms"

    if( 'status_code' in test['response'] ):
        req['result']['status_code'] = ("FAILED", "OK")[ int(response.status_code) == int(test['response']['status_code']) ]
    
    if( 'body' in test['response'] ):
        req['result']['body'] = ("FAILED", "OK")[ response.json() == test['response']['body'] ]
    
    return req


#Function to build the html page
def generate_body(tests_info,results):
    template = Template(page)
    return template.render(test_name = tests_info["name"], test_url = tests_info["base_url"], tests = results)


# Function to get the current timestamp
def now():
    a = datetime.datetime.now()
    return a

def check_url(base_url, mini_url):

    #check url formmating

    #base_url

    if mini_url.startswith("http"):
        return mini_url

    elif mini_url.startswith("/"):

        complete_url = base_url + mini_url
        complete_url = complete_url.replace("//","/")

        return complete_url
        
    else:
        return(base_url + mini_url)
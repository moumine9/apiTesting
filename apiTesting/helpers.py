#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import faker
import datetime
import requests
import termtables
from requests_ntlm import HttpNtlmAuth
from datetime import timedelta
from jinja2 import Template
from yaml import load, dump
from colorama import Fore, Back, Style, init, AnsiToWin32

init(autoreset=True)

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

def failed():
    return Back.RED + Fore.WHITE + " FAILED " + Style.RESET_ALL

def success():
    return Back.BLACK + Fore.GREEN + "SUCCESS" + Style.RESET_ALL

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

    if  mini_url.find("http://") != -1:
        return mini_url

    elif mini_url[0] == "/":
        complete_url = base_url + mini_url[1:]
        return complete_url

    else:
        return(base_url + mini_url)

def authentication(auth):
    if(auth["method"] == "none"):
        return None
    
    elif(auth["method"] == "HttpNtlmAuth"):
        params = auth['params']
        params = json.loads( params.replace("\'", "\"") )
        return HttpNtlmAuth(params['user'],params['pass'])
        

def execute_tests(tests_data, auth):
    
    tests_results = []

    for test in tests_data["test_cases"]:

        if ( test['method'] in ('POST', 'PUT', 'UPDATE', 'PATCH') and ('data' not in test) ):
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
            req = requests.get( complete_url, headers = {'content-type': 'application/json'}, auth= authentication(auth) )
        
        tests_results.insert(-1,clean_response(req, test, ( now() - start ) ))    

    return tests_results



def display_log(tests_results):

    header = ["Url", "Method", "Result"]
    data = []
    
    for test in tests_results:
        res = "N/A"
        status_code = test['result']['status_code']
        body = test['result']['body']

        if( (status_code == body == "OK") or (status_code == body == "N/A")  ):
            res = success()
        elif( status_code == "OK" and body == "N/A" ):
            res = success()
        elif( status_code == "N/A" and body == "OK" ):
            res = success()
        else:
            res = failed()
            
        data.insert(-1, [ test["url"], test["method"], res ])


    string = termtables.to_string(
        data,
        header=header,
        style=termtables.styles.ascii_thin,
        padding=(0, 1)
    )

    print(string)


def export_results(outputfile, tests_info, tests_results):
    
    if outputfile.find("htm") != -1:
        page = generate_body(tests_info,tests_results)
        output = open(outputfile,'w')
        output.write(page)
        return True

    elif outputfile.find("csv") != -1:
        output = open(outputfile,'w')
        output.write("Name,Url,method,Result,Time\n")

        for t in tests_results:
            result = ("OK","FAILED")[ t["result"]["status_code"] == 'FAILED' or t["result"]["body"] == 'FAILED']
            output.write("%s,%s,%s,%s,%s\n" % (t["name"], t["url"], t["method"], result, t["time"] ) )

        return True

    elif (outputfile.find("yaml") != -1) or (outputfile.find("yml") != -1):
        yml_version = dump(tests_results)
        output = open(outputfile,'w')
        output.write(yml_version)

        return True
    
    elif outputfile.find("json") != -1:
        json_version = json.dumps(tests_results)
        output = open(outputfile,'w')
        output.write(json_version)
        
        return True
    
    else:
        return False

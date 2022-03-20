#!/usr/bin/python3
# -*- coding: utf-8 -*-
from cryptography.fernet import Fernet
import requests
from json import loads as jsonload
import argparse
import os


'''
pyskytapapi.py is to be used by other python modules to automate skytap api usage.
it could be called in command line.
See Skytap official references to get the correct Api URL and method to use :
    V1 : https://help.skytap.com/API_Documentation.html
    V2 : https://help.skytap.com/API_v2_Documentation.html
 
By default, the V1 API is used. Using -v2 option, the V2 API is used. 

DISCLAIMER: I didn't test the DELETE Operation (the skytap environment is not mine!)

Examples : default /templates
GET /templates : list templates

    python3 pyskytapapi.py 

GET /users : list all users

    python3 pyskytapapi.py -a /users -m GET


GET /users/{user-id}.json : get user details

    python3 pyskytapapi.py -a /users/{user-id}.json -m GET

POST /configurations.json : create a new configuration

    python3 pyskytapapi.py -m POST -J configurations.json -a /configurations.json

DELETE /configurations/{configuration-id} : delete the resource

    python3 pyskytapapi.py -m DELETE -a /configurations/{configuration-id}

PUT /configurations/{configuration-id}: update the resource 

    python3 pyskytapapi.py -m PUT -J {configuration-id}.json -a /configurations/{configuration-id} 

    
'''

__version__ = "1.0.1"

ALLOWED_METHODS = ["DELETE", "GET", "POST", "PUT"]
URL = "https://cloud.skytap.com"
NO_CONTENT = 204

def pyskytapApiVersion():
    return f"pyskytapapi version : {__version__}"


class skytapApi():
    def __init__(self, api, method, url, user, token, jsonfile):
        self.api = api
        self.method = method
        self.json = jsonfile
        self.url = url
        self.user = user
        self.token = skytapApi.crypted(token)


    def __repr__(self):
        return (f"skytapApi api: {self.api}, method: {self.method}, url: {self.url}")

    #return the encrypted password/token
    @classmethod
    def crypted(cls, token):
        cls.privkey = Fernet.generate_key()        
        cipher_suite = Fernet(cls.privkey)
        ciphered_text = cipher_suite.encrypt(token.encode())
        cls.token = ciphered_text
        return cls.token

    #return the decrypted password/token
    @classmethod
    def decrypted(cls, token):
        cls.token = token
        cipher_suite = Fernet(cls.privkey)
        decrypted_text = cipher_suite.decrypt(cls.token)
        decrypted_text = decrypted_text.decode()
        return decrypted_text

    #execute the skytap api using a temp instance
    @staticmethod
    def runskytapApi(api, method, url, user, token, json):
        if token == None:
            response = jsonload('{"message": "Error : token missing!"}')
            return response 
        tempskytap = skytapApi(api, method, url, user, token, json)
        response = tempskytap.skytapAuthentication()
        tempskytap = None
        return response       


    #call private function
    def skytapAuthentication(self):
        response = self.__skytapTokenAuth()
        return response

    #internal function that formats the url and calls the skytap apis
    def __skytapTokenAuth(self):
        apiurl = self.url + self.api  
        header = {}
        header['Accept'] = 'application/json'
        header['Content-Type'] = 'application/json'
        auth =  (self.user, skytapApi.decrypted(self.token))  
        response = self.__skytapDispatch(apiurl, auth, header)
        return response

    #internal function that calls the requests
    def __skytapDispatch(self, apiurl, auth, header):
        response = "{}"        
        try:
            if self.method == "POST":
                contents = open(self.json, 'r')
                response = requests.post(apiurl, auth=auth, headers=header, data=contents)
                contents.close()
            elif self.method == "GET":
                response = requests.get(apiurl, auth=auth, headers=header)
            elif self.method == "PUT":
                if self.json == '':
                    response = requests.put(apiurl, auth=auth,  headers=header)
                else:
                    contents = open(self.json, 'r')                    
                    response = requests.put(apiurl, auth=auth,  headers=header, data=contents)
                    contents.close()
            elif self.method == "DELETE":
                #raise Exception("DELETE not implemented yet")
                response = requests.delete(apiurl, auth=auth, headers=header)  
        except requests.exceptions.RequestException as e:  
            raise SystemExit(e)   
        if response.status_code == NO_CONTENT:
            response = "{}"
        elif response.status_code != 200:
            response = jsonload('{"message": "Error : ' + str(response.status_code) + ' ' + response.reason + '"}')
        else:            
            response = response.json()
        return response

def pyskytapapi(args):
    message = ''
    if args.user == '':
        user = os.environ.get("SKYTAP_USER")
    else:
        user = args.user  
    if args.token == '':
        itoken = os.environ.get("SKYTAP_TOKEN")
    else:
        itoken = args.token               
    if args.api == '' and args.jsonfile == '':
        api=f"/templates"
    else:
        api=args.api    
    if args.url == '':
        iurl = URL
    else:
        iurl = args.url        
    method = args.method     
    if args.v2 == True:
        iurl = URL + "/v2"
    if "POST" in method and args.jsonfile == "":
        print("Json file required with method POST!")
        return
    json = args.jsonfile        
    message= skytapApi.runskytapApi(api=api, method=method, url=iurl, user=user, token=itoken, json=json ) 
    return message


if __name__== "__main__":
    helpmethod = f"should contain one of the method to use : {str(ALLOWED_METHODS)}"
    parser = argparse.ArgumentParser(description="pyskytapapi is a python3 program that call skytap apis in command line or imported as a module")
    parser.add_argument('-V', '--version', help='Display the version of pyskytapapi', action='version', version=pyskytapApiVersion())
    parser.add_argument('-U', '--user', help='skytap user', default='', required=False)    
    parser.add_argument('-t', '--token', help='skytap token', default='', required=False)    
    parser.add_argument('-u', '--url', help='skytap url', default='', required=False)    
    parser.add_argument('-a', '--api', help='skytap api should start by a slash', default='', required=False)    
    parser.add_argument('-m', '--method', help = helpmethod, default="GET", required=False)   
    parser.add_argument('-J', '--jsonfile', help='json file needed for POST method', default='', required=False)
    parser.add_argument('-v2', help='api version V2 to use', action="store_true", required=False)
    args = parser.parse_args()
    message = pyskytapapi(args)
    print(message)
# pyskytapapi
python3 module to call skytap api in command line or inside a module.  


## pyskytapapi.py


usage: pyskytapapi.py [-h] [-V] [-U USER] [-t TOKEN] [-u URL] [-a API] [-m METHOD] [-J JSONFILE] [-v2]

pyskytapapi is a python3 program that call skytap apis in command line or imported as a module

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Display the version of pyskytapapi
  -U USER, --user USER  skytap user
  -t TOKEN, --token TOKEN
                        skytap token
  -u URL, --url URL     skytap url
  -a API, --api API     skytap api should start by a slash
  -m METHOD, --method METHOD
                        should contain one of the method to use : ['DELETE', 'GET', 'POST', 'PUT']
  -J JSONFILE, --jsonfile JSONFILE
                        json file needed for POST method
  -v2                   api version V2 to use


## release notes

pyskytapapi.py

1.0.0 initial version
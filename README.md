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



## examples 

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


## release notes

pyskytapapi.py

1.0.0 initial version
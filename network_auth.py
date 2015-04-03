#!/usr/bin/python
# Authenticates against a LAN using HTTP Basic Auth

import sys

if len(sys.argv) != 4:
    print ("Invalid arguments")
    print ("Proper syntax is: " + sys.argv[0] + " [url] [username] [password]")
    sys.exit(1)

import requests
import requests.exceptions

auth_target = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

print ("Checking connection to: " + auth_target)

try:
    auth_check = requests.get(auth_target)
except requests.exceptions.ConnectionError as e:
    print (e)
    sys.exit(2)
except requests.exceptions.Timeout as e:
    print (e)
    sys.exit(3)
except Exception as e:
    print (e)
    sys.exit(98)

check_status = auth_check.status_code
print ("Response status code is: " + str(check_status))

if check_status == 200:
    print ("You are already authenticated")
    sys.exit(0)

print ("Authenticating...")

try:
    do_auth = requests.get(auth_target, auth=(username, password))
except requests.exceptions.ConnectionError as e:
    print (e)
    sys.exit(4)
except requests.exceptions.Timeout as e:
    print (e)
    sys.exit(5)
except Exception as e:
    print (e)
    sys.exit(99)

auth_status = do_auth.status_code
if auth_status == 200:
    print ("Authentication successful")
else:
    print ("Authentication failed with response code: " + str(auth_status))


#!/usr/bin/python
# Authenticates against a LAN using HTTP Basic Auth

import sys, argparse, logging, requests, requests.exceptions

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logFile')
    parser.add_argument('url')
    parser.add_argument('username')
    parser.add_argument('password')
    args = parser.parse_args()

    auth_target = args.url
    username = args.username
    password = args.password
    logFile = args.logFile

    requests.packages.urllib3.disable_warnings()
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

    if logFile:
        logging.basicConfig(filename=logFile, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    if "http" not in auth_target:
        log('URI not fully defined, adding "http://"')
        auth_target = "http://" + auth_target

    log('Checking connection to: ' + auth_target, printToScreen=True)

    try:
        auth_check = requests.get(auth_target, timeout=10, verify=False)
    except requests.exceptions.Timeout as e:
        log('Connection timeout, server offline? ', logLevel='ERROR', printToScreen=True)
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        log('Connection Error, invalid domain?', logLevel='ERROR', printToScreen=True)
        sys.exit(1)
    except Exception as e:
        log(e, logLevel='ERROR', printToScreen=True)
        sys.exit(1)

    check_status = auth_check.status_code
    log('Response status code is: ' + str(check_status), printToScreen=True)

    if check_status == 200:
        log('You are already authenticated', printToScreen=True)
        sys.exit(0)

    log('Authenticating...', printToScreen=True)

    try:
        do_auth = requests.get(auth_target, auth=(username, password), timeout=10, verify=False)
    except requests.exceptions.Timeout as e:
        log('Connection timeout, server offline? ', logLevel='ERROR', printToScreen=True)
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        log('Connection Error, invalid domain?', logLevel='ERROR', printToScreen=True)
        sys.exit(1)
    except Exception as e:
        log(e, logLevel='ERROR', printToScreen=True)
        sys.exit(1)

    auth_status = do_auth.status_code
    if auth_status == 200:
        log('Authentication successful', printToScreen=True)
    else:
        log('Authentication failed with response code: ' + str(auth_status), logLevel='WARNING', printToScreen=True)

def log(message, logLevel='INFO', printToScreen=False):
    if logLevel.upper() == 'DEBUG':
        logging.debug(message)
    elif logLevel.upper() == 'WARNING':
        logging.warning(message)
    elif logLevel.upper() == 'ERROR':
        logging.error(message)
    elif logLevel.upper() == 'CRITICAL':
        logging.critical(message)
    else:
        logging.info(message)

    if printToScreen:
        print(message)

if __name__ == "__main__":
   main(sys.argv[1:])

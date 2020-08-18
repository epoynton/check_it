#!/usr/bin/env python3
# checks email or list of emails against HIBP
# thanks to https://github.com/m0nkeyplay for

import requests
import json
import os
import time
import argparse

def show_help():
    print('\n::Help with argument usage::\n')
    print('Are you searching one or many emails?')
    print('-e  or -f with textFile having one email per line')
    print('$: Breach+Email: check_it.py -b -e my@email.com')
    print('$: Breach+List of emails: check_it.py -b -f ./path/to/file')

ap = argparse.ArgumentParser()
ap.add_argument("-b", "--breach", action="store_true")
ap.add_argument("-e", "--email", required=False, help="Search for just one email")
ap.add_argument("-f", "--file", required=False, help="grab emails from a list of files -f /path/to/file")
args = vars(ap.parse_args())

if args['breach']:
    hibpCheck = 'breachaccount'
else:
    show_help()
    exit()

if args['email']:
      chkType = 'email'
      chkIt = args['email']
elif args['file']:
      chkType = 'file'
      chkIt = args['file']

headers = {}
headers['content-type']= 'application/json'
headers['api-version']= '3'
headers['User-Agent']='check_it'
#   Place that API key here
headers['hibp-api-key']='a921ff8eb0124346a5ceff4b87aa596a'

# Check Breach
def check_breach(email):
    url = 'https://haveibeenpwned.com/api/v3/breachedaccount/'+email+'?truncateResponse=false'
    r = requests.get(url, headers=headers)
    if r.status_code == 404:
        print("%s not found in a breach."%email)
    elif r.status_code == 200:
        data = r.json()
        print('Breach Check for: %s'%email)
        for d in data:
            breach = d['Name']
            domain = d['Domain']
            description = d['Description']
            breachDate = d['BreachDate']
            sensitive = d['IsSensitive']
            print('Account: %s\nBreach: %s\nSensitive: %s\nDomain: %s\nBreach Date:%s\nDescription: %s\n'%(email,breach,sensitive,domain,breachDate,description))
            #   or to print out the whole shebang comment above and uncomment below
            #for k,v in d.items():
            #    print(k+":"+str(v))
    else:
        data = r.json()
        print('Error: <%s>  %s'%(str(r.status_code),data['message']))
        exit()

if __name__ == '__main__':
    # Single Checks
    if chkType == 'email':
        if hibpCheck == 'breachaccount':
            check_breach(chkIt)
        else:
            print("what did you want to search?")
    # File Checks
    elif chkType == 'file':
        if not os.path.isfile(chkIt):
            print('\n\nWe can\'t find/open %s.  Please check that it\'s a valid file.\n\n'%chkIt)
        else:
            get_emails = open(chkIt, 'r')
            for line in get_emails:
                cleanEmail = line.strip()
                if hibpCheck == 'breachaccount':
                    check_breach(cleanEmail)
                    time.sleep(2)
                else:
                    check_paste(cleanEmail)
                    time.sleep(2)
            get_emails.close()
    # Something really interesting happened
    else:
        print('definitely pwned...')

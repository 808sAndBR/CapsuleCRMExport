import requests
import json
import csv

# Get your auth code from the user page in CapsuleCRM
authCode = 'YOURAUTHCODEHERE'

# Get a list of all companies in your Capsule
url = 'https://piazza.capsulecrm.com/api/party/'
headers = {'Accept': 'application/json'}
r = requests.get(url,headers=headers,auth=(authCode, 'x'))

capsuleIDs = []

for company in r.json()['parties']['organisation']:
    capsuleIDs.append(company['id'])

allData = []
allData.append(['noteId','partyId','partyName','entryDate','creatorName','subject','note'])

# Itterate through all your companies and get the corespondences for each
for company in capsuleIDs:
    url = 'https://piazza.capsulecrm.com/api/party/'+str(company)+'/history'
    headers = {'Accept': 'application/json'}
    r = requests.get(url,headers=headers,auth=('af14cfcc22c4be843992c1130a791505', 'x'))
    partyContact = r.json()
# Capsule will treat a single corespondance as a dict and multiple as a list, below deals with that
    try:
        if str(type(partyContact['history']['historyItem'])) == "<type 'dict'>":
            x = partyContact['history']['historyItem']
            allData.append([x['id'],x['partyId'],x['partyName'].encode('ascii','ignore'),x['entryDate'],x['creatorName'],x['subject'].encode('ascii','ignore'),x['note'].encode('ascii','ignore')])
            print x['partyName']
            print '^^^^^^^^^^^^^^^^^^^'
        else:
            for contact in partyContact['history']['historyItem']:
                    allData.append([contact['id'],contact['partyId'],contact['partyName'].encode('ascii','ignore'),contact['entryDate'],contact['creatorName'],contact['subject'].encode('ascii','ignore'),contact['note'].encode('ascii','ignore')])
                    print contact['partyName']
                    print '---------------'
    except KeyError:
        print company

# write all the data we pulled as a csv
with open('companyNotes.csv', 'wb') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(allData)

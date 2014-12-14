import requests
import json
import csv 

# Get your auth code from the user page in CapsuleCRM
authCode = 'YOURAUTHCODEHERE'

# Get a list of all people in your Capsule
url = 'https://piazza.capsulecrm.com/api/party/'
headers = {'Accept': 'application/json'}
r = requests.get(url,headers=headers,auth=(authCode, 'x'))

allPeople = []

for people in r.json()['parties']['person']:
    allPeople.append(people['id'])

  
allData = []
allData.append(['noteID','partyId','partyName','entryDate','creatorName','subject','note'])

# Itterate through all your people and get the corespondences for each
for company in allPeople:
    url = 'https://piazza.capsulecrm.com/api/party/'+str(company)+'/history'
    headers = {'Accept': 'application/json'}
    r = requests.get(url,headers=headers,auth=('af14cfcc22c4be843992c1130a791505', 'x'))
    partyContact = r.json()
    try:
# Capsule will treat a single corespondance as a dict and multiple as a list, below deals with that
        if str(type(partyContact['history']['historyItem'])) == "<type 'dict'>":
            x = partyContact['history']['historyItem']
            dataSet1 = [x['id'],x['partyId'],x['partyName'].encode('ascii','ignore'),x['entryDate'],x['creatorName'],x['subject'].encode('ascii','ignore'),x['note'].encode('ascii','ignore')]
            dataSet2 = []
# Capsule will treat a single participant as a dict and multiple as a list, below deals with that
            if str(type(x['participants'])) == "<type 'dict'>":
                    dataSet2.append(x['participants']['role'])
                    dataSet2.append(x['participants']['emailAddress'])
            else:
                for people in x['participants']:
                    dataSet2.append(people['role'])
                    dataSet2.append(people['emailAddress'])
                dataJoined = dataSet1 + dataSet2
            allData.append(dataJoined)
            print x['partyName']
            print '^^^^^^^^^^^^^^^^^^^'
        else:
            for contact in partyContact['history']['historyItem']:
                dataSet1 = [contact['id'],contact['partyId'],contact['partyName'].encode('ascii','ignore'),contact['entryDate'],contact['creatorName'],contact['subject'].encode('ascii','ignore'),contact['note'].encode('ascii','ignore')]
                dataSet2 = []
                if str(type(contact['participants'])) == "<type 'dict'>":
                        dataSet2.append(contact['participants']['role'])
                        dataSet2.append(contact['participants']['emailAddress'])
                else:                    
                    for people in contact['participants']:
                        dataSet2.append(people['role'])
                        dataSet2.append(people['emailAddress'])
                    dataJoined = dataSet1 + dataSet2
                    allData.append(dataJoined)
                    print contact['partyName']
                    print '---------------'
    except KeyError:
        print company

# write all the data we pulled as a csv
with open('individualNotes.csv', 'wb') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(allData)
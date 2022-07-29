import requests
import json
import math
import pandas as pd
import sys

if(len(sys.argv) < 2):
    raise Exception("Usage: python <filename>.py \"Industry Name\"")

url = "https://uktiersponsors.co.uk/tierapi/api/tierData/Companies"

payload = json.dumps({
    "PageNumber": 0,
    "RowsPerPage": 20,
    "Town": "London",
    "Industry": sys.argv[1]
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

totalCount = response.json()['count']
companyMasterList = []

print("Total Expected Iterations: "+ str(math.ceil(totalCount/20)))
for i in range(0,math.ceil(totalCount/20)):
    print("------------Fetching Companies for "+str(i)+"th iteration start-----------")
    perPagePayload = json.dumps({
        "PageNumber": i,
        "RowsPerPage": 20,
        "Industry": sys.argv[1],
        "Town": "London"
    })
    perPageResponse = requests.request("POST", url, headers=headers, data=perPagePayload).json()
    
    for company in perPageResponse['companies']:
        transformedCompany = {}
        transformedCompany['Company Name'] = company['organisationName']
        transformedCompany['Visa Tier'] = company['mainTier'] + '-'+company['subTier']
        transformedCompany['City'] = company['town']
        transformedCompany['Date Added'] = company['dateAdded']
        transformedCompany['Website'] = company['website']
        transformedCompany['LinkedIn'] = company['socialWebsite']
        companyMasterList.append(transformedCompany)
    print("Company Master List Size: "+str(len(companyMasterList)))
    print("------------Fetching Companies for "+str(i)+"th iteration end-----------")

df = pd.DataFrame(companyMasterList)
df.to_csv(sys.argv[1]+'-UK.csv', index=False)

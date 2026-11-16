import requests

# GET request

query_params = {
    'query.lead' : 'pfizer',
    'pageSize' : 1
}
response = requests.get("https://clinicaltrials.gov/api/v2/studies", params=query_params)

print(response.status_code)
#print(response.text)
#print(response.content)
print(len(response.json()))
print(response.json().keys())
print(len(response.json()['studies']))
#print(response.json()['studies'][0])
study = response.json()['studies'][0]
print(study.keys())
print(study['protocolSection']['identificationModule'])
print('NCT ID: ', study['protocolSection']['identificationModule']['nctId'])
print('title overview: ', study['protocolSection']['identificationModule']['briefTitle'])
print('specific title: ', study['protocolSection']['identificationModule']['officialTitle'])
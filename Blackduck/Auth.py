import requests
import json

#Input Variables

#Blackduck URL
hub_uri = ''

#API Token
apitoken = ''

# Set the request headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'token {apitoken}'
}
response = requests.post(f'{hub_uri}/api/tokens/authenticate', headers=headers)
if response.status_code == 200:
    bearertoken = response.json()['bearerToken']
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f'bearer {bearertoken}'
    }
    #Make API Call Here and Uncomment Lines 21-25
    #response = requests.get(f'{hub_uri}/api/', headers=headers)
    #if response.status_code == 200:
        #print(response.json())
    #else:
        #print(response.status_code, response.json()['errorMessage'])
else:
    if response.status_code == 401:
        print(response.status_code, response.json()['errorMessage'])
        print('Check API Token and User Permissions')
    #print(response.status_code, response.json()['errorMessage'])

import requests
import json

hub_uri = ''
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
	response = requests.get(f'{hub_uri}/api/current-user/tokens', headers=headers)
	tokenjson = response.json()
	for item in tokenjson['items']:
		href_value = item['_meta']['href']
		urls = href_value
		print(urls)
		for url in urls:
			headers = {
			"Accept": "/",
			"Content-Type": "/",
			"Authorization": f'bearer {bearertoken}'
			}
			response = requests.delete(urls, headers=headers)
















import requests
import base64
import json
 

#Variables to Input:
api_token= "i6lnkpoj8l69l2bp3m3g6ukj1jq6cvjbic2kt9s0q0r5di1dec11903spgu622krm0j5biep6km4c"

#Do Not Touch
portfoliourl = "https://poc.polaris.synopsys.com/api/portfolio/portfolios"
applicationurl = "https://poc.polaris.synopsys.com/api/portfolio/portfolios/{portfolioid}/portfolio-items"


headers = {
"accept": "application/vnd.synopsys.pm.portfolio-1+json",
"Api-Token": api_token
}
portfolioresponse = requests.get(portfoliourl, headers=headers)
if portfolioresponse.status_code == 200:
	portfolioid = portfolioresponse.json()['_items'][0]['id']
	headers = {
	"accept": "application/vnd.synopsys.pm.portfolio-items-1+json",
	"Content-Type": "application/vnd.synopsys.pm.portfolio-items-1+json",
	"Api-Token": api_token
	}
	applicationresponse = requests.get(f"https://poc.polaris.synopsys.com/api/portfolio/portfolios/{portfolioid}/portfolio-items", headers=headers)
	if applicationresponse.status_code == 200:
		print(applicationresponse.json())
		
		
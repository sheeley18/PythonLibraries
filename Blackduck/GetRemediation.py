import requests
import json
import re
import argparse

#TO DO:
#1. Line 113 fix json parsing so longterm and shortterm version names return
#2. Escape Loop checking for transitives and get normal upgrade guidance instead

#Input Variables

#Blackduck URL
hub_uri = 'URL'

#API Token
apitoken = 'API Token'

# Set up argument parsing
parser = argparse.ArgumentParser(description='Process project Name.')
parser.add_argument('--Project', required=True, help='The Project to list Version IDs for')
parser.add_argument('--Version', required=True, help='The Version to list Component IDs for')
args = parser.parse_args()

# Get the Project from the command-line arguments
projectName = args.Project

# Get the Project from the command-line arguments
versionName = args.Version

# Set the request headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'token {apitoken}'
}
response = requests.post(f'{hub_uri}/api/tokens/authenticate', headers=headers)
if response.status_code == 200:
    projectsearch_terms = f"name:{projectName}"
    params = {
    'limit': 50,
    }
    bearertoken = response.json()['bearerToken']
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f'bearer {bearertoken}'
    }
    #Get Project ID
    response = requests.get(f"{hub_uri}/api/projects?q={projectsearch_terms}", headers=headers, params=params)
    if response.status_code == 200:
        versionsearch_terms = f"versionName:{versionName}"
        projectdata = response.json()
        projectID = projectdata['items'][0]['_meta']['href'].split("/")[-1]
        headers = {
        "Accept": "application/vnd.blackducksoftware.project-detail-5+json",
        "Content-Type": "application/vnd.blackducksoftware.project-detail-5+json",
        "Authorization": f'bearer {bearertoken}'
        }
        #Get Version ID
        response = requests.get(f"{hub_uri}/api/projects/{projectID}/versions?q={versionsearch_terms}", headers=headers)
        if response.status_code == 200:
            versiondata = response.json()
            versionID = versiondata['items'][0]['_meta']['href'].split("/")[-1]
            #print(versionID)
            params = {
            'limit': 1000,
            }
            headers = {
            "Accept": "application/vnd.blackducksoftware.bill-of-materials-6+json",
            "Content-Type": "application/vnd.blackducksoftware.bill-of-materials-6+json",
            "Authorization": f'bearer {bearertoken}'
            }
            #Get Component ID, Version ID and Origin
            print("Direct Dependency Guidance") 
            directresponse = requests.get(f"{hub_uri}/api/projects/{projectID}/versions/{versionID}/components?filter=bomMatchType:file_dependency_direct&filter=securityRisk:critical&filter=securityRisk:high&filter=securityRisk:medium&filter=securityRisk:low", headers=headers, params=params)
            if directresponse.status_code == 200:
                directcomponentdata = directresponse.json()
                if directcomponentdata['items']:
                    for item in directcomponentdata['items']:
                        match_type = item['matchTypes']
                        component_name = item["componentName"]
                        componentId = item["component"].split("/")[-1]
                        version_name = item.get("componentVersionName")
                        origin_id_string = [origin["origin"].split("/")[-1].split("[")[-1] for origin in item["origins"]]
                        origin_id = str(origin_id_string).replace('[', '').replace(']', '').replace("'", '')
                        componentVersionId = item.get("componentVersion")
                        if componentVersionId:
                            versionId = componentVersionId.split('/')[-1]
                            if item['matchTypes'] == ['FILE_DEPENDENCY_DIRECT']:
                                match_type = item['matchTypes']
                                component_name = item["componentName"]
                                componentId = item["component"].split("/")[-1]
                                version_name = item["componentVersionName"]
                                componentVersionId = item["componentVersion"].split("/")[-1]
                                origin_id_string = [origin["origin"].split("/")[-1].split("[")[-1] for origin in item["origins"]]
                                origin_id = str(origin_id_string).replace('[', '').replace(']', '').replace("'", '')
                                #print(f"Component Name: {component_name} | Component ID: {componentId} | Component Version Name {version_name} | Version ID {componentVersionId}")
                                params = {
                                'limit': 1000,
                                }
                                headers = {
                                "Accept": "application/vnd.blackducksoftware.component-detail-5+json",
                                "Content-Type": "application/vnd.blackducksoftware.component-detail-5+json",
                                "Authorization": f'bearer {bearertoken}'
                                }
                                response = requests.get(f"{hub_uri}/api/components/{componentId}/versions/{versionId}/origins/{origin_id}/upgrade-guidance", headers=headers, params=params)
                                if response.status_code == 200:
                                    upgradedata = response.json()
                                    versionName = upgradedata['versionName']
                                    componentName = upgradedata['componentName']
                                    componentVersion = upgradedata['versionName']
                                    short_term = upgradedata.get('shortTerm')
                                    long_term = upgradedata.get('longTerm')
                                    if short_term:
                                        short_term_version_name = short_term.get('versionName')
                                        if long_term:
                                            long_term_version_name = long_term.get('versionName')
                                            print(f"Component Name: {component_name} | Current Version: {versionName} | Short Term: {short_term_version_name} | Long Term: {long_term_version_name}")
                                        else:
                                            print(response.status_code, response.json()['errorMessage'])



            else:
                print(response.status_code, response.json()['errorMessage'])
        else:
            print(response.status_code, response.json()['errorMessage'])
    else:
        print(response.status_code, response.json()['errorMessage'])
else:
    if response.status_code == 401:
        print(response.status_code, response.json()['errorMessage'])
        print('Check API Token and User Permissions')
    #print(response.status_code, response.json()['errorMessage'])
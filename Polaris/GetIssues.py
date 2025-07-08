import requests

# === Required inputs ===
API_TOKEN = "Access Token"
PROJECT_ID = "ProjectID"  # Replace this with your known projectId

# === Polaris API endpoint and headers ===
BASE_URL = "https://poc.polaris.blackduck.com"
ISSUES_ENDPOINT = f"{BASE_URL}/api/findings/issues"
HEADERS = {
    "Api-Token": API_TOKEN,
    "Accept": "application/vnd.polaris.findings.issues-1+json",
    "Accept-Language": "en-CA,en;q=0.9"
}

# === Optional query flags ===
QUERY_PARAMS = {
    "projectId": PROJECT_ID,
    "_includeType": "true",
    "_includeOccurrenceProperties": "true",
    "_includeTriageProperties": "true",
    "_includeFirstDetectedOn": "true",
    "_includeIssueExclusion": "true",
    "_first": 500  # You can paginate further if needed
}

def get_issues():
    response = requests.get(ISSUES_ENDPOINT, headers=HEADERS, params=QUERY_PARAMS)
    if response.status_code != 200:
        print(f"Failed to fetch issues: {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    return data.get("_items", [])

def main():
    issues = get_issues()
    print(f"Retrieved {len(issues)} issues.\n")

    for issue in issues:
        ctx = issue.get("context", {})
        print(f"Issue Key: {issue.get('issueKey')}")
        print(f"  Severity: {issue.get('severity')}")
        print(f"  Type: {issue.get('issueType')}")
        print(f"  File: {ctx.get('filePath')}")
        print(f"  Line: {ctx.get('line')}")
        print(f"  First Detected On: {issue.get('firstDetectedOn')}")
        print(f"  Occurrence Properties: {issue.get('occurrenceProperties', [])}")
        print(f"  Triage: {issue.get('triageProperties', [])}")
        print("—" * 40)

if __name__ == "__main__":
    main()


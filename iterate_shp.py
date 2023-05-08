import requests
import json

# Set the SharePoint site URL
site_url = "https://yourdomain.sharepoint.com/sites/YourSiteName"

# Set the client ID and client secret
client_id = "your_client_id_here"
client_secret = "your_client_secret_here"

# Construct the authorization header
auth_url = "https://accounts.accesscontrol.windows.net/yourdomain.onmicrosoft.com/tokens/OAuth/2"
auth_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "resource": "00000003-0000-0ff1-ce00-000000000000/yourdomain.sharepoint.com@yourdomain.onmicrosoft.com"
}
auth_response = requests.post(auth_url, data=auth_data)
auth_response.raise_for_status()
access_token = auth_response.json()["access_token"]
headers = {
    "Authorization": "Bearer " + access_token,
    "Accept": "application/json;odata=verbose"
}

# Make the API request to get the list of directories
api_url = site_url + "/_api/web/Lists/getByTitle('Documents')/RootFolder?$expand=Folders,Folders/Folders"
api_response = requests.get(api_url, headers=headers)
api_response.raise_for_status()

# Parse the API response and print the list of directories
api_data = api_response.json()
folders = api_data["Folders"]
print("List of Directories:")
for folder in folders:
    print(folder["Name"])
    subfolders = folder["Folders"]
    for subfolder in subfolders:
        print("  " + subfolder["Name"])


import requests
import adal
import json

# Replace the placeholders with your own values
site_url = 'https://your-sharepoint-site.sharepoint.com'
library_path = '/sites/your-site/your-library/'
file_name = 'your-file.docx'
tenant_id = 'your-tenant-id'
client_id = 'your-client-id'
client_secret = 'your-client-secret'

# Get an access token
authority_url = 'https://login.microsoftonline.com/' + tenant_id
resource_url = site_url
context = adal.AuthenticationContext(authority_url)
token = context.acquire_token_with_client_credentials(resource_url, client_id, client_secret)

# Download the file
file_url = site_url + library_path + file_name
response = requests.get(file_url, headers={'Authorization': 'Bearer ' + token['accessToken']}, stream=True)

# Save the file to disk
with open(file_name, 'wb') as f:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)

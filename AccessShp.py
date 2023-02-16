import requests

# Replace the placeholders with your own values
site_url = 'https://your-sharepoint-site.sharepoint.com'
file_url = 'https://your-sharepoint-site.sharepoint.com/sites/your-site/your-library/your-file.docx'
username = 'your-username'
password = 'your-password'

# Get the authentication token
auth_url = f'{site_url}/_api/contextinfo'
headers = {'accept': 'application/json;odata=verbose'}
response = requests.post(auth_url, headers=headers, auth=(username, password))
response_data = response.json()
form_digest_value = response_data['d']['GetContextWebInformation']['FormDigestValue']

# Download the file
file_data = requests.get(file_url, headers={
    'accept': 'application/json;odata=verbose',
    'Authorization': f'Bearer {form_digest_value}'
}, auth=(username, password))

# Save the file to disk
with open('your-file.docx', 'wb') as f:
    f.write(file_data.content)

###In this example, the code first gets an authentication token from SharePoint using the _api/contextinfo endpoint. It then uses this token to download the file from the given file URL. Finally, the downloaded file is saved to the local disk.

###Make sure to replace the placeholders with your own values before running the code. Also note that you will need to have the requests library installed in your Python environment.





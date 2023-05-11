import requests

# SharePoint site URL
site_url = 'https://your-sharepoint-site-url.com'

# SharePoint site relative URL of the .doc file
doc_file_url = '/sites/your-site/your-library/your-file.doc'

# SharePoint site relative URL to the SharePoint REST API endpoint
api_url = '/_api/web/GetFileByServerRelativeUrl(\'{}\')/\$value'.format(doc_file_url)

# SharePoint site relative URL of the target PDF file
pdf_file_url = '/sites/your-site/your-library/your-file.pdf'

# SharePoint app client ID
client_id = 'your-client-id'

# SharePoint app client secret
client_secret = 'your-client-secret'

# Get access token
auth_url = 'https://accounts.accesscontrol.windows.net/{tenant_id}/tokens/OAuth/2'
auth_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
auth_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'resource': site_url,
}
auth_response = requests.post(auth_url.format(tenant_id='common'), headers=auth_headers, data=auth_data).json()
access_token = auth_response['access_token']

# Convert the .doc file to .pdf using SharePoint REST API
pdf_headers = {'Authorization': 'Bearer {}'.format(access_token)}
pdf_response = requests.post(site_url + api_url, headers=pdf_headers)

# Save the PDF file to SharePoint
save_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/octet-stream',
    'X-RequestDigest': requests.post(site_url + '/_api/contextinfo', headers=pdf_headers).json()['d']['GetContextWebInformation']['FormDigestValue'],
}
with open('your-file.pdf', 'wb') as f:
    f.write(pdf_response.content)
save_response = requests.post(site_url + pdf_file_url + '/content', headers=save_headers, data=pdf_response.content)

print(save_response.status_code)

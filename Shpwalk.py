import json

# Define function to get directory structure recursively
def print_directory_structure(url, access_token, indent=0):
    response = requests.get(url, headers={'Authorization': f'Bearer {access_token}'})
    response.raise_for_status()
    data = response.json()
    for item in data['value']:
        print(' ' * indent + item['Name'])
        if item['Folder']:
            print_directory_structure(item['@odata.id'], access_token, indent + 2)

# Call function to print directory structure
print_directory_structure(f'{site_url}/_api/web/GetFolderByServerRelativeUrl(\'/\')/Folders', access_token)

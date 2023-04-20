import requests
from requests.auth import HTTPBasicAuth
import json
import io
import zipfile

# set the SharePoint site url and credentials
site_url = "https://your_sharepoint_site_url"
username = "your_username"
password = "your_password"

# function to get the contents of a folder
def get_folder_contents(folder_url):
    # set the REST API endpoint for getting the contents of a folder
    endpoint_url = site_url + "/_api/web/GetFolderByServerRelativeUrl('" + folder_url + "')?$expand=Folders,Files"
    
    # make a GET request to the endpoint to get the folder contents
    response = requests.get(endpoint_url, auth=HTTPBasicAuth(username, password))
    
    # parse the response as JSON
    data = json.loads(response.text)
    
    # get the subfolders and files of the folder
    subfolders = data['d']['Folders']['results']
    files = data['d']['Files']['results']
    
    # print the subfolders and files
    print("Subfolders:")
    for folder in subfolders:
        print(" - " + folder['Name'])
    print("Files:")
    for file in files:
        print(" - " + file['Name'])
        # if the file is a zip file, extract its contents by folder name
        if file['Name'].endswith(".zip"):
            extract_zip_contents(file['ServerRelativeUrl'])

# function to extract the contents of a zip file by folder name
def extract_zip_contents(file_url):
    # set the REST API endpoint for getting the contents of a file
    endpoint_url = site_url + "/_api/web/GetFileByServerRelativeUrl('" + file_url + "')/$value"
    
    # make a GET request to the endpoint to get the file contents
    response = requests.get(endpoint_url, auth=HTTPBasicAuth(username, password))
    
    # read the file contents as a zip file
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    
    # get the names of all the folders in the zip file
    folder_names = set()
    for filename in zip_file.namelist():
        if filename.endswith("/"):
            folder_names.add(filename[:-1])
    
    # extract the contents of each folder in the zip file
    for folder_name in folder_names:
        print("Folder: " + folder_name)
        for filename in zip_file.namelist():
            if filename.startswith(folder_name + "/") and not filename.endswith("/"):
                print(" - " + filename[len(folder_name) + 1:])
    
    # close the zip file
    zip_file.close()

# call the get_folder_contents function to start listing down the contents of the root folder
get_folder_contents("/")

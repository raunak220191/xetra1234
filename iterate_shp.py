import requests
from requests.auth import HTTPBasicAuth
import json

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

# function to recursively list down all directories and files
def list_folders_and_files(folder_url):
    # set the REST API endpoint for getting the contents of a folder
    endpoint_url = site_url + "/_api/web/GetFolderByServerRelativeUrl('" + folder_url + "')?$expand=Folders,Files"
    
    # make a GET request to the endpoint to get the folder contents
    response = requests.get(endpoint_url, auth=HTTPBasicAuth(username, password))
    
    # parse the response as JSON
    data = json.loads(response.text)
    
    # get the subfolders and files of the folder
    subfolders = data['d']['Folders']['results']
    files = data['d']['Files']['results']
    
    # print the folder name and its contents
    print("Folder: " + data['d']['Name'])
    print("Subfolders:")
    for folder in subfolders:
        print(" - " + folder['Name'])
    print("Files:")
    for file in files:
        print(" - " + file['Name'])
    
    # ask the user to select a subfolder to view its contents
    while True:
        selection = input("Enter a subfolder name to view its contents (or type 'exit' to quit): ")
        if selection == "exit":
            return
        for folder in subfolders:
            if folder['Name'] == selection:
                # if the user selected a subfolder, recursively list down its contents
                list_folders_and_files(folder['ServerRelativeUrl'])
                break
        else:
            print("Invalid selection. Please try again.")

# call the list_folders_and_files function to start listing down the folders and files
list_folders_and_files("/")

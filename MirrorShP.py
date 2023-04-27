from shareplum import Site
from shareplum import Office365
import os

# SharePoint site URL
site_url = "https://your.sharepoint.site/"

# Client ID and client secret
client_id = "<your-client-id>"
client_secret = "<your-client-secret>"

# Local folder path to mirror SharePoint folder
local_folder_path = "/path/to/local/folder/"

# SharePoint folder URL
sharepoint_folder_url = "/Shared Documents"

# Create an Office365 object with the site URL, client ID, and client secret
authcookie = Office365(site_url, client_id=client_id, client_secret=client_secret).GetCookies()
site = Site(site_url, authcookie=authcookie)

# Function to download a file from SharePoint
def download_file(file_url, local_path):
    with open(local_path, 'wb') as local_file:
        file_content = site.download(file_url)
        local_file.write(file_content)

# Function to download a folder from SharePoint
def download_folder(folder_url, local_path):
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    folder = site.GetFolderByServerRelativeUrl(folder_url)
    files = folder.files
    for file in files:
        file_url = file.ServerRelativeUrl
        file_name = os.path.basename(file_url)
        local_file_path = os.path.join(local_path, file_name)
        download_file(file_url, local_file_path)
    subfolders = folder.folders
    for subfolder in subfolders:
        subfolder_url = subfolder.ServerRelativeUrl
        subfolder_name = os.path.basename(subfolder_url)
        subfolder_local_path = os.path.join(local_path, subfolder_name)
        download_folder(subfolder_url, subfolder_local_path)

# Download the SharePoint folder and all its subfolders and files
download_folder(sharepoint_folder_url, local_folder_path)

import os
import json
import requests

def upload_file(file_path, token=None, folder_id=None):
    # Get the server address
    response = requests.get("https://api.gofile.io/getServer")
    if response.status_code != 200:
        raise Exception("Failed to get server address")

    server = response.json().get("data", {}).get("store8")
    if not server:
        raise Exception("Server address not found")

    # Prepare the upload URL
    upload_url = f"https://{server}.gofile.io/uploadFile"

    # Prepare the files and data
    files = {'file': open(file_path, 'rb')}
    data = {}
    if token:
        data['token'] = token
    if folder_id:
        data['folderId'] = folder_id

    # Perform the upload request
    response = requests.post(upload_url, files=files, data=data)
    if response.status_code != 200:
        raise Exception("Failed to upload file")

    # Clean up
    os.remove(file_path)

    # Process the response
    response_data = response.json()
    if response_data["status"] == "ok":
        data = response_data["data"]
        data["directLink"] = f"https://{server}.gofile.io/download/{data['fileId']}/{data['fileName']}"
        return data
    elif "error-" in response_data["status"]:
        error = response_data["status"].split("-")[1]
        raise Exception(error)
    else:
        raise Exception("Unexpected response status")


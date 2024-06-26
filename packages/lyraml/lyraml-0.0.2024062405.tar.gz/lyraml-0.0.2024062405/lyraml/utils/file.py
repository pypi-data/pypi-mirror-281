import requests
import json
from urllib.parse import quote_plus, parse_qs
from .constants import BASE_URL

# TODO: Need to include projectId? Otherwise, users can just download any code source code
def upload_data(filename, data, api_key):
    encoded_filename = quote_plus(filename)
    signed_url_response = requests.get(BASE_URL + "/signed_upload_url?filename=" + encoded_filename, headers={'Authorization': f'Bearer {api_key}'})
    if signed_url_response.status_code != 200:
        raise ValueError("Failed to create signed url.")
    
    signed_url_body = json.loads(signed_url_response.text)
    signed_url = signed_url_body["signedUrl"]
    if type(data) is str:
        upload_response = requests.put(signed_url, data=data.encode('utf-8'), headers={'Content-Type': 'application/octet-stream'})
    if type(data) is dict:
        upload_response = requests.put(signed_url, data=data, headers={'Content-Type': 'application/octet-stream'})

    if upload_response.status_code != 200:
        raise ValueError("Failed to upload data")
    
    return filename

def download_data(filename, api_key):
    encoded_filename = quote_plus(filename)
    download_response = requests.get(BASE_URL + "/signed_download_url?filename=" + encoded_filename, headers={'Authorization': f'Bearer {api_key}'})
    if download_response.status_code != 200:
        raise ValueError("Failed to download " + filename)
    
    download_response_body = json.loads(download_response.text)
    signed_url = download_response_body["signedUrl"]

    headers = {'Content-Type': 'application/octet-stream'}

    content_response = requests.get(signed_url, headers=headers)
    return content_response.text

def read_source_code_as_func(source_code, func_name):
    local_env = {}
    exec(source_code, {}, local_env)

    # Return the function object from the local_env dictionary
    # The name for "scoring_rubric" should be dynamic
    return local_env[func_name]
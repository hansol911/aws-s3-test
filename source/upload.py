import boto3
import json
import base64
import requests
from requests_toolbelt.multipart import decoder


def upload_file_to_s3(file, presignedURL):
    url = presignedURL['content'].decode('utf-8')
    content = file['content']
    type = file['type'].decode('utf-8')
    
    response = requests.put(url, data=content, headers={'Content-Type' : type})
    
    return None
    
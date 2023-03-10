import boto3
import json
import base64
from requests_toolbelt.multipart import decoder
import validate
#import upload

def lambda_handler(event, context):
    content_type_header = event['headers']['content-type']
    files = get_multipart_file(event['body'], content_type_header)
    
    return create_response(result)
    
    
def create_response(result):
    return {
        "statusCode": result['statusCode'],
        "body": json.dumps({
            "result": result['message']}),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
    }
    
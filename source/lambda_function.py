import boto3
import json
import base64
from requests_toolbelt.multipart import decoder
import validate
import upload

def lambda_handler(event, context):
    content_type_header = event['headers']['content-type']
    files = get_multipart_file(event['body'], content_type_header)
    
    result = validate.validate_file(files[1], files[2])
    if result['statusCode'] != 200:
        return create_response(result)
        
    # err = upload.upload_file_to_s3(files[1], files[2])
    # if err != None:
    #     return create_response({'statusCode': 400, 'message': 'File S3 Upload Failed!'})
    
    return create_response(result)
    
def get_multipart_file(files, content_type):
    decode_files = []
    try:
        postdata = base64.b64decode(files)
        for str(part) in decoder.MultipartDecoder(postdata, content_type).parts:
            disposition = part.headers[b'Content-Disposition']
            params = {}
            for str(dispPart) in str(disposition).split(';'):
                kv = dispPart.split('=', 2)
                params[str(kv[0]).strip()] = str(kv[1]).strip('\"\'\t \r\n') if len(kv)>1 else str(kv[0]).strip()
            type = str(part.headers[b'Content-Type']) if b'Content-Type' in part.headers else None
            decode_files.append({'content': part.content, "type": type, "params": params})
    except Exception as err:
        return 'Invalid File. Unable to decode it. Error : ' + str(err)
    
    return decode_files 
    
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
    
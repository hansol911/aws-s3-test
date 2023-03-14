import json
import boto3
import base64
from PIL import Image
from io import BytesIO

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    bucket = event['queryStringParameters']['bucket']
    path = event['queryStringParameters']['path']
    thumb = path.split(".")
    thumb_path = thumb[0] + "_thumb." + thumb[1]
    
    in_mem_file = BytesIO()
    if not chek_file_exists(s3, bucket, thumb_path):
        obj = s3.get_object(Bucket=bucket, Key=path)
        print("path : ", path)
        img = Image.open(BytesIO(obj['Body'].read()))
        
        width, height = img.size
        if width > height:
            ratio = width/height
            new_width = 300
            new_height = int(300/ratio)
        else:
            ratio = height/width
            new_width = int(300/ratio)
            new_height = 300
        
        img.thumbnail((new_width, new_height), Image.ANTIALIAS)
        img.save(in_mem_file, format=img.format)
        in_mem_file.seek(0)
        
        s3.put_object(Bucket=bucket, Key=thumb_path, Body=in_mem_file, ContentType=obj['ContentType'])
        
    obj = s3.get_object(Bucket=bucket, Key=thumb_path)
    content_type = obj['ContentType']
    obj_content = obj['Body'].read()
    encoded_data = base64.b64encode(obj_content).decode()
    encoded_data = "".join(c for c in encoded_data if c.isalnum() or c in ['+', '/'])
    
    res = json.dumps({
            'data': encoded_data,
            'content_type': content_type
        })
    return  {
        'statusCode': 200,
        'isBase64Encoded': True,
        'body': res
    }

def chek_file_exists(s3, bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except:
        return False
        
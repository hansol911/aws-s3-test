import json
import boto3
import test
from PIL import Image
from io import BytesIO

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    bucket = event['queryStringParameters']['bucket']
    path = event['queryStringParameters']['path']
    thumb = path.split(".")
    thumb_path = thumb[0] + "_thumb." + thumb[1]
    
    in_mem_file = BytesIO()

    obj = s3.get_object(Bucket=bucket, Key=path)
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


    result = test.test_str('abc')
    return {
        'statusCode': 200,
        'body': result,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
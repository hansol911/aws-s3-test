import json
import boto3
import re

def check_filename(presigned_url, file):
    try:
        s3 = boto3.client('s3')

        url_parts = presigned_url.split("/")
        bucket = url_parts[2].split(".")[0]
        key = "/".join(url_parts[3:])
        key = key.split("?")[0]
        
        while True:
            try:
                response = s3.head_object(Bucket=bucket, Key=key)
                match = re.search(r'\((\d+)\)', key)
                if match:
                    i = int(match.group(1)) + 1
                    key = re.sub(r'\(\d+\)', f"({i})", key)
                else:
                    key = key.split(".")
                    key = f"{key[0]} (1).{key[1]}"
            except:
                break

        content = file['content']
        type = str(file['type'].decode('utf-8'))
        
        s3.put_object(Bucket=bucket, Key=key, Body=content, ContentType=type)
        
        return key
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
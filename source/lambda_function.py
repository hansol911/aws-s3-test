import json
import test

def lambda_handler(event, context):
    result = test.test_str('abc')
    return {
        'statusCode': 200,
        'body': result,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
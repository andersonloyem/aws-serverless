### import package
import boto3
from boto3.dynamodb.conditions import Key
import json, re, uuid
import os
import logging

# init ressource
dynamodb = boto3.client('dynamodb')
dynamodb2 = boto3.resource('dynamodb')
tableName = os.environ["TABLE"]
table = dynamodb2.Table(tableName)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):    
    data = event
    print(data)
    ins = dict()
    
    try :
        personItem    = table.query(KeyConditionExpression=Key('id').eq(data['id'])).get('Items')[0]
        personItem    = (personItem)
        print("personItem")
        print(personItem)
        response = {
            "statusCode": 200,
            "body": dict(version="v1", success=True, error_code=200, message=None, data=personItem)
        }
        return response
    except Exception as e:
        print("Except : "+str(e))
        response = {
            "statusCode": 500,
            "body": dict(version="v1", success=False, error_code=500, message=str(e), data=None)
        }
        logger.error(response)
        return response
        

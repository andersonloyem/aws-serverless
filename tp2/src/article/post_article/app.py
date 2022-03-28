import boto3
import os
import json
import uuid
from datetime import datetime


def lambda_handler(event, context):

    if ('body' not in event):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    table_name = os.environ.get('TABLE', 'Article')
    region = os.environ.get('REGION', 'eu-west-3')
    aws_environment = os.environ.get('AWSENV', 'AWS')

    if aws_environment == 'AWS_SAM_LOCAL':
        article_table = boto3.resource(
            'dynamodb',
            endpoint_url='http://dynamodb:8000'
        )
    else:
        article_table = boto3.resource(
            'dynamodb',
            region_name=region
        )

    table = article_table.Table(table_name)
    activity = json.loads(event['body'])

    params = {
        'id': str(uuid.uuid4()),
        'date': str(datetime.timestamp(datetime.now())),
        'stage': activity['stage'],
        'description': activity['description']
    }

    response = table.put_item(
        TableName=table_name,
        Item=params
    )
    print(response)

    return {
        'statusCode': 201,
        'headers': {},
        'body': json.dumps({'msg': 'Article created'})
    }
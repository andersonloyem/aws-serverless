import boto3
import os
import json
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):

    if ('pathParameters' not in event):
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
    article_id = event['pathParameters']['id']

    response = table.query(
        KeyConditionExpression=Key('id').eq(article_id)
    )
    print(response)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(response['Items'])
    }
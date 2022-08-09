### import package
import boto3
import json, re, uuid
import os
import logging
#from country import get_country

# init ressource
dynamodb = boto3.client('dynamodb')
dynamodb2 = boto3.resource('dynamodb')
tableName = os.environ["TABLE"]
table = dynamodb2.Table(tableName)
lambdaFunction = boto3.client('lambda')
s3 = boto3.client('s3')
bucket = os.environ["bucket_person"]
countryFunctionArn = os.environ["lambda_country"]

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        data = event
        logger.info(data)
        for field in ["nom", "prenom", "dateNaissance", "photo"]:
            if not data.get(field):
                response = {
                    "statusCode": 500,
                    "body": dict(version="v1", success=False, error_code=500, message=f"{field} is not present", data=None)
                }
                logger.error(response)
                return response
        id = generateID()
        nom     = data["nom"] 
        prenom  = data["prenom"]
        dateNaissance = data["dateNaissance"]
        photo   = data["photo"]
        country = call_function()
        pays = json.loads(country['Payload'].read().decode()) 
        pays = pays.get('body').get('country')  

        item = dict(id=id, nom=nom, prenom=prenom, dateNaissance=dateNaissance, pays=pays)
        writeFileInS3(bucket, id+".txt", photo)
        table.put_item(Item=item)
        response = {
            "statusCode": 200,
            "body": dict(version="v1", success=True, error_code=200, message=None, data=item)
        }
        logger.info(response)
        return response
        
    except Exception as err:  
        response = {
            "statusCode": 500,
            "body": dict(version="v1", success=False, error_code=500, message=str(err), data=None)
        }
        logger.error(response)
        return response

def generateID() :
    ID = str(uuid.uuid4())
    ID = re.sub("\D","",ID)[:4]
    isExist = dynamodb.get_item(TableName=tableName, Key={'id': { 'S':ID}})
       
    while not isExist.get("Item") is None :
        ID = str(uuid.uuid4())
        ID = re.sub("\D","",ID)[:4]
        isExist = dynamodb.get_item(TableName=tableName, Key={'id': { 'S':ID}})

    return ID

def writeFileInS3(bucket, fileName, data) :
    
    client = boto3.client('s3')
    client.put_object(
        Body=data, 
        Bucket=bucket, 
        Key=fileName,
        ContentEncoding='base64',
        )
    return 1

def call_function(functionArn = countryFunctionArn) :
    data = dict()
    return lambdaFunction.invoke(
        FunctionName=functionArn, 
        InvocationType='RequestResponse',
        Payload = json.dumps(data) 
        )
import json
from country import get_country


def lambda_handler(event, context):
    
    return {
        "statusCode": 200,
        "body":{
            "country": get_country()[1],
            "country-code": get_country()[0],
        },
    }

import json
import boto3

def prepareResponse(event, response):
    response = {
                "sessionState": {
                    "dialogAction": {
                    "type": "Close"
                    },
                    "intent": {
                    "name": event['sessionState']['intent']['name'],
                        "state": "Fulfilled"
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": str(response)
                    }
                ]
            }
    
    return response

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('cityDistances')

    try: 
        city1 = event['sessionState']['intent']['slots']['source']['value']['interpretedValue']
        city2 = event['sessionState']['intent']['slots']['destination']['value']['interpretedValue']
    except:
        return {
            "statusCode": 400, 
            "body": "There Are No Parameters", 
        }

    cityKey = city1 + ", " + city2

    if city1 == city2:
        return prepareResponse(event, 0)

    try:
        while True:
            scan_kwargs = {}
            response = table.scan(**scan_kwargs)
            items = response['Items']

            for item in items:
                if cityKey == item['cityToCity']:
                    return prepareResponse(event, item['distance'])
            
            if 'LastEvaluatedKey' not in response:
                break
            scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
            
        return prepareResponse(event, -1)

    except Exception as e:
        return {
            "statusCode": 400, 
            "body": f"Error: {e}"
        }
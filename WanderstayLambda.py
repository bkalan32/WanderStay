import json
import datetime
import time

def validate(slots):
    
    # Define Valid Cities
    
    valid_cities = ["detroit", "phoenix", "houston", "dallas"]
    
    if not slots["Location"]:
        print("Location Not Found")
        return {
        'isValid': False,
        'violatedSlot': 'Location'
        }
    
    if slots['Location']['value']['originalValue'].lower() not in valid_cities:
        
        print("Not a valid location")
        
        return {
        'isValid': False,
        'violatedSlot': 'Location',
        'message': 'We currently support only {} as a valid destination.'.format(", ".join(valid_cities))
        }
    
    if not slots['CheckInDate']:
        
        return{
        'isValid': False,
        'violatedSlot': 'CheckInDate'
        }
        
    if not slots ["Nights"]:
        return{
        'isValid': False,
        'violatedSlot': 'Nights',
        }
    if not slots ['RoomType']:
        return{
        'isValid': False,
        'violatedSlot': 'RoomType'
        }
        
    return {'isValid': True}
        
def lambda_handler(event, context):
    # Access 'invocationSource' using 'get' with a default value of None
    invocation_source = event.get('invocationSource', None)

    if invocation_source == 'DialogCodeHook':
        slots = event.get('sessionState', {}).get('intent', {}).get('slots', {})
        intent = event.get('sessionState', {}).get('intent', {}).get('name', None)
        print(invocation_source)
        print(slots)
        print(intent)
        validation_result = validate(slots)

        if not validation_result['isValid']:
            if 'message' in validation_result:
                response = {
                    'sessionState': {
                        'dialogAction': {
                            'slotToElicit': validation_result["violatedSlot"],
                            'type': "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": validation_result["message"]
                        }
                    ]
                }
            else:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": validation_result['violatedSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    }
                }
            return response
        else:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        "name": intent,
                        "slots": slots
                    }
                }
            }
            return response

    elif invocation_source == 'FulfillmentCodedHook':
        # Add order in Database
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent,
                    "slots": slots,
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Thanks, I have placed your reservation"
                }
            ]
        }
        return response

    else:
        # Handle unknown or missing 'invocationSource' logic
        return {
            "errorMessage": "Invalid invocationSource",
            "errorType": "InvalidInvocationSourceError",
            "requestId": context.aws_request_id
        }
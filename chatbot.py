import json

def validate(slots):
    if not slots['Location']:
        print("Inside Empty Location")
        return {
            'isValid': False,
            'violatedSlot': 'Location'
        }        
    if not slots['CheckInDate']:
        return {
            'isValid': False,
            'violatedSlot': 'CheckInDate',
        }   
    if not slots['Nights']:
        return {
            'isValid': False,
            'violatedSlot': 'Nights'
        }
        
    if not slots['RoomType']:
        return {
            'isValid': False,
            'violatedSlot': 'RoomType'
        }

    return {'isValid': True}

def lambda_handler(event, context):

    # Add error handling for missing sessionState or intent keys
    try:
        slots = event['sessionState']['intent']['slots']
        intent = event['sessionState']['intent']['name']
    except KeyError as e:
        print(f"Error: Missing key in event - {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps("Error: Missing required fields in event")
        }
    
    print(event['invocationSource'])
    print(slots)
    validation_result = validate(slots)
    print(validation_result)
    
    # Handling DialogCodeHook
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            response =  {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit': validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }
        else:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots   
                    }
                }
            }

    # Handling FulfillmentCodeHook
    if event['invocationSource'] == 'FulfillmentCodeHook':
        # Add order in Database here
        
        # Final response with thank you message
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    'name': intent,
                    'slots': slots
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Thank you for confirming your booking! Your reservation has been successfully placed."
                }
            ]
        }
    
    return response

# -*- coding: utf-8 -*-

import json
from web_flyer import WebFlyer, WebFlyerError, ExternalServiceError

def lambda_handler(event, context):
    origin = event['pathParameters']['origin']
    destination = event['pathParameters']['destination']
    try:
        api = WebFlyer(origin=origin, destination=destination)
        return { 'statusCode': 200, 'body': json.dumps({'miles': api.miles}) }
    except WebFlyerError as e:
        return { 'statusCode': 400, 'body': json.dumps({'error': e.msg}) }
    except ExternalServiceError as e:
        return { 'statusCode': 500, 'body': json.dumps({'error': e.msg}) }


if __name__ == '__main__':
    event = {
        'pathParameters': {
            'origin': 'SAN',
            'destination': 'PDX',
        },
        'queryStringParameters': None,
    }
    print('{!r}'.format(lambda_handler(event, None)))

    event = {
        'pathParameters': {
            'origin': 'SFO',
            'destination': 'LAX',
        },
        'queryStringParameters': None,
    }
    print('{!r}'.format(lambda_handler(event, None)))

    event = {
        'pathParameters': {
            'origin': 'SFO',
            'destination': 'XXX',
        },
        'queryStringParameters': None,
    }
    print('{!r}'.format(lambda_handler(event, None)))

    event = {
        'pathParameters': {
            'origin': 'SFO',
            'destination': 'L',
        },
        'queryStringParameters': None,
    }
    print('{!r}'.format(lambda_handler(event, None)))

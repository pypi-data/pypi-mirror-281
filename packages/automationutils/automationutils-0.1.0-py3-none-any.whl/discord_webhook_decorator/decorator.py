import functools
import requests
import json


def discord_webhook(webhook_url, payload):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if callable(payload):
                data = payload(result)
            else:
                data = payload

            headers = {
                'Content-Type': 'application/json',
            }
            response = requests.post(webhook_url, data=data, headers=headers)

            if response.status_code != 204:
                print(f'Failed to send discord message. Status code: {response.status_code}')
                print(response.text)
            return result
        return wrapper
    return decorator


import requests
import json 


api_key = 'fItY1aFCge0vQZRKKdh5tIthyGfTdhLb'


def extract():
    response = requests.get(f'https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key={api_key}')
    if response.status_code == 200:
        json_data = response.json()
        data = json.dumps(json_data)
        print(data)
    else:
        print('Failed to extract...')

extract()
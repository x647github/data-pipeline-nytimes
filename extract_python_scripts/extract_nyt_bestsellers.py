from dotenv import load_dotenv
import os
import requests
import json 


load_dotenv()
api_key = os.getenv('API_KEY')


def extract():
    response = requests.get(f'https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key={api_key}')
    if response.status_code == 200:
        json_data = response.json()
        data = json.dumps(json_data)
        print(data)
    else:
        print('Failed to extract...')

extract()

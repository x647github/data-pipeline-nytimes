from dotenv import load_dotenv
import os
from datetime import date
import requests
import json 


current_day = date.today()
year, month = current_day.year, current_day.month

load_dotenv()
api_key = os.getenv('API_KEY')

def extract():
    response = requests.get(f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={api_key}')
    if response.status_code == 200:
        json_data = response.json()
        data = json.dumps(json_data)
        print(data)
    else:
        print('Failed to extract...')

extract()

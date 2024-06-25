import dotenv
import json
import os
import requests

from dotenv import load_dotenv

load_dotenv()

EDAMAM_APP_ID = os.getenv('EDAMAM_APP_ID')
EDAMAM_APP_KEY = os.getenv('EDAMAM_APP_KEY')


def get_recipe(dish):
    EDAMAM_URL = "https://api.edamam.com/api/recipes/v2"

    auth_response = requests.get(EDAMAM_URL, {
        'type': 'public',
        'q': dish,
        'app_id': EDAMAM_APP_ID,
        'app_key': EDAMAM_APP_KEY,
    })

    # print(auth_response.json())
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(auth_response.json(), f, ensure_ascii=False, indent=4)

    return dish

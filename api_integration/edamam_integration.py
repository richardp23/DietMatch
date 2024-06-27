import json
import requests


def get_recipe(app_id, app_key, dish):
    EDAMAM_URL = "https://api.edamam.com/api/recipes/v2"

    auth_response = requests.get(EDAMAM_URL, {
        'type': 'public',
        'q': dish,
        'app_id': app_id,
        'app_key': app_key,
    })

    # # print(auth_response.json())
    # with open('data.json', 'w', encoding='utf-8') as f:
    #     json.dump(auth_response.json(), f, ensure_ascii=False, indent=4)

    # return dish

    recipe = auth_response.json()['hits'][0]['recipe']
    recipe_name = recipe['label']
    ingredient_lines = recipe['ingredientLines']

    recipe_details = recipe_name
    for ingredient in ingredient_lines:
        recipe_details += f"\n{ingredient}"

    return recipe_details

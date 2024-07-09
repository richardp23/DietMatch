import json
import requests

# from db.recipe_sql import store_original_recipe


def get_recipe(app_id, app_key, dish):
    EDAMAM_URL = "https://api.edamam.com/api/recipes/v2"

    auth_response = requests.get(EDAMAM_URL, {
        'type': 'public',
        'q': dish,
        'app_id': app_id,
        'app_key': app_key,
    })
    
    auth_response.raise_for_status() 


    data = auth_response.json()

    if 'hits' in data and data['hits']:
        recipe = data['hits'][0]['recipe']
        recipe_name = recipe['label']
        ingredient_lines = recipe['ingredientLines']
        recipe_url = recipe['url']

        # store_original_recipe(recipe_name, ingredient_lines, recipe_url)

        recipe_details = {
            'name': recipe_name,
            'ingredients': ingredient_lines,
            'url': recipe_url
        }

        return recipe_details
    else:
        return None


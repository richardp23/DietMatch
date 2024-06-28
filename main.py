import dotenv
import sqlite3
import os

from dotenv import load_dotenv
from api_integration.edamam_integration import get_recipe
from api_integration.openai_integration import alt_recipe_query
from db.recipe_sql import (
    create_tables, store_original_recipe, 
    store_alt_recipe, lookup_prev_recipe, 
    reset_database)

# Importing env variables for API authentication
load_dotenv()
EDAMAM_APP_ID = os.getenv('EDAMAM_APP_ID')
EDAMAM_APP_KEY = os.getenv('EDAMAM_APP_KEY')
OPENAI_KEY = os.getenv('OPENAI_KEY')


def main():
    print("Welcome to DietMatch!")

    while True:
        print("What would you like to do?")

        choice = input(
            "Type \"make\" to make a recipe,"
            " \"lookup\" to find a previously made recipe,"
            " \"exit\" to quit the program! "
            "or \"reset\" to clear database "
        )

        if choice.lower() == "reset":
            reset_database()
        elif choice.lower() == "make":
            make_recipe()
        elif choice.lower() == "lookup":
            lookup_prev_recipe()
        elif choice.lower() == "exit":
            break
        else:
            print("Choice not valid, please try again!\n")


def make_recipe():
    diet = input("\nPlease tell me what kind of diet you follow: ")
    requested_recipe = input("Please tell me what kind of dish you would like to make: ")

    recipe_query = get_recipe(EDAMAM_APP_ID, EDAMAM_APP_KEY, requested_recipe)
    original_name = recipe_query['name']
    ingredients = []
    for ingredient in recipe_query['ingredients']:
        ingredients.append(ingredient)
    recipe_link = recipe_query['url']
    store_original_recipe(original_name, ingredients, recipe_link)
    
    alt_recipe = alt_recipe_query(OPENAI_KEY, diet, recipe_query)
    alt_name = alt_recipe['name']
    alt_ingredients = alt_recipe['ingredients']
    alt_instructions = alt_recipe['instructions']

    original_recipe_id = lookup_original_recipe_id(original_name, ingredients, recipe_link)
    store_alt_recipe(original_recipe_id, alt_name, alt_ingredients, alt_instructions)

    print(f"\nAlternative Recipe: {alt_name}\nIngredients: {', '.join(alt_ingredients)}\nInstructions: {alt_instructions}\n")


def lookup_original_recipe_id(name, ingredients, recipe_link):
    ingredients_str = ', '.join(ingredients)

    with sqlite3.connect('recipes.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM original_recipes WHERE name = ? AND ingredients = ? AND recipe_link = ?', (name, ingredients_str, recipe_link))
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            raise ValueError("Original recipe not found in the database.")
    


if __name__ == "__main__":
    create_tables()
    main()

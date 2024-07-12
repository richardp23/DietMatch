import dotenv
import sqlite3
import os

from dotenv import load_dotenv

from api_integration.edamam_integration import get_recipe
from api_integration.openai_integration import alt_recipe_query
from db.recipe_sql import (create_tables, store_original_recipe, store_alt_recipe, lookup_prev_recipe, select_recipe, reset_database)

# Importing env variables for API authentication
load_dotenv()
EDAMAM_APP_ID = os.getenv('EDAMAM_APP_ID')
EDAMAM_APP_KEY = os.getenv('EDAMAM_APP_KEY')
OPENAI_KEY = os.getenv('OPENAI_KEY')


def main(action, *args):
    create_tables()
    if action.lower() == "reset":
        reset_database()
    elif action.lower() == "make":
        return make_recipe(args[0], args[1])
    elif action.lower() == "lookup":
        return lookup_db(args[0]) if args else lookup_db()
    elif action.lower() == "exit":
        exit()
    else:
        print("Choice not valid, please try again!\n")


def make_recipe(diet, requested_recipe):
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

    return f"\nAlternative Recipe: {alt_name}\nIngredients: {', '.join(alt_ingredients)}\nInstructions: {alt_instructions}\n"
    # print(f"\nAlternative Recipe: {alt_name}\nIngredients: {', '.join(alt_ingredients)}\nInstructions: {alt_instructions}\n")


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


def lookup_db(recipe_id = None):
    if recipe_id:
        return select_recipe(recipe_id)
    else:
        foundRecipes, recipes = lookup_prev_recipe()
        if foundRecipes and __name__ == "__main__":
            try:
                recipe_id = int(input("Enter the ID of the recipe you want to view: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                return
            select_recipe(recipe_id)
        else:
            return recipes
    

if __name__ == "__main__":
    print("Welcome to DietMatch!")

    while True:
        print("What would you like to do?")

        choice = input(
            "Type \"make\" to make a recipe,"
            " \"lookup\" to find a previously made recipe,"
            " \"exit\" to quit the program,"
            " or \"reset\" to clear database! "
        )

        if choice == "make":
            diet = input("\nPlease tell me what kind of diet you follow: ")
            requested_recipe = input("Please tell me what kind of dish you would like to make: ")
            result = main(choice, diet, requested_recipe)
            if result:
                print(result)
            else:
                print("Recipe creation failed or returned empty result.")
        else:
            print(main(choice))
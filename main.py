import dotenv
import os

from dotenv import load_dotenv
from edamam_integration import get_recipe
from openai_integration import alt_recipe_query

# Importing env variables for API authentication
load_dotenv()
EDAMAM_APP_ID = os.getenv('EDAMAM_APP_ID')
EDAMAM_APP_KEY = os.getenv('EDAMAM_APP_KEY')
OPENAI_KEY = os.getenv('OPENAI_KEY')


def main():
    print("Welcome to DietMatch!")

    diet = input("\nPlease tell me what kind of diet you follow: ")
    requested_recipe = input(
        "Please tell me what kind of"
        " dish you would like to make: ")

    recipe_query = get_recipe(EDAMAM_APP_ID, EDAMAM_APP_KEY, requested_recipe)
    print(f"\n{alt_recipe_query(OPENAI_KEY, diet, recipe_query)}")


if __name__ == "__main__":
    main()

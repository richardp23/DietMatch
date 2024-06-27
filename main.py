import dotenv
import os

from dotenv import load_dotenv
from api_integration.edamam_integration import get_recipe
from api_integration.openai_integration import alt_recipe_query

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
            " or \"exit\" to quit the program! "
        )

        if choice.lower() == "make":
            make_recipe()
        elif choice.lower() == "lookup":
            lookup_prev_recipe()
        elif choice.lower() == "exit":
            exit
        else:
            print("Choice not valid, please try again!\n")


def make_recipe():
    diet = input("\nPlease tell me what kind of diet you follow: ")
    requested_recipe = input(
        "Please tell me what kind of"
        " dish you would like to make: ")

    recipe_query = get_recipe(EDAMAM_APP_ID, EDAMAM_APP_KEY, requested_recipe)
    new_recipe = f"\n{alt_recipe_query(OPENAI_KEY, diet, recipe_query)}\n"
    print(new_recipe)


def lookup_prev_recipe():
    return True


if __name__ == "__main__":
    main()

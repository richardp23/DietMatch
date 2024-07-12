import openai
from openai import OpenAI


def alt_recipe_query(key, diet, recipe_query):
    client = OpenAI(api_key=key)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content":
                    "You are a skilled dietitian who can provide any type of"
                    " cooking recipes and alternatives for different diets. "
                    "Return the prompt with the alternate recipe name in"
                    " quotes."
                    "I am looking to make the following recipe, "
                    "with alternative ingredients that fit into a "
                    f"{diet} diet.",
            },
            {"role": "user", "content": recipe_query['name']}
        ]
    )

    alt_recipe_content = completion.choices[0].message.content

    def parse_alternative_recipe_string(recipe_string):
        alt_name = ""
        alt_ingredients = ""
        alt_instructions = ""

        alt_name_start = recipe_string.find('"') + 1
        alt_name_end = recipe_string.find('"', alt_name_start)
        if alt_name_start != -1 and alt_name_end != -1:
            alt_name = recipe_string[alt_name_start:alt_name_end].strip()

        ingredients_start = (
            recipe_string.find("Ingredients:") + len("Ingredients:")
        )
        ingredients_end = recipe_string.find("Instructions:")

        if ingredients_start != -1 and ingredients_end != -1:
            ingredients_section = (
                recipe_string[ingredients_start:ingredients_end].strip()
            )
            alt_ingredients = [
                '\n ' + line.strip() for line in
                ingredients_section.splitlines() if line.strip()
                ]
            formatted_ingredients = ''.join(alt_ingredients)

        instructions_start = (
            recipe_string.find("Instructions:") + len("Instructions:")
        )
        if instructions_start != -1:
            instructions_section = recipe_string[instructions_start:].strip()
            instructions_lines = instructions_section.splitlines()
            formatted_instructions = []
            step_number = 1
            for line in instructions_lines:
                if line.strip().startswith(str(step_number) + "."):
                    formatted_instructions.append(line.strip())
                    step_number += 1
                else:
                    formatted_instructions[-1] += " " + line.strip()
            alt_instructions = "\n" + "\n".join(formatted_instructions)

        return alt_name, alt_ingredients, alt_instructions

    alt_name, alt_ingredients, alt_instructions = (
        parse_alternative_recipe_string(alt_recipe_content)
    )

    alt_recipe = {
        'name': alt_name,
        'ingredients': alt_ingredients,
        'instructions': alt_instructions
    }

    return alt_recipe

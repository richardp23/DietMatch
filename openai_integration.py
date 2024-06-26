import openai
from openai import OpenAI


def alt_recipe_query(key, diet, recipe):
    # Setup for API auth
    client = OpenAI(
        api_key=key,
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content":
                "You are a skilled dietian who can provide any type of"
                " cooking recipes and alternatives for different diets. "
                "I am looking to make the following recipe, with alternative"
                f" ingredients that fit into a {diet} diet."},
            {"role": "user", "content": recipe}
        ]
    )
    return completion.choices[0].message.content

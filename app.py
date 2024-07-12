from flask import Flask, render_template, request, jsonify

from main import main

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/create-recipe", methods=['GET', 'POST'])
def create_recipe():
    if request.method == 'POST':
        print("testing")
        diet_preference = request.form.get('diet-preference')
        original_recipe = request.form.get('original-recipe')

        print(request.form)
        
        # Process the data (for example, generate a recipe)
        generated_recipe = main("make", diet_preference, original_recipe)
        
        return render_template('create_recipe.html', generated_recipe=generated_recipe)
        
    return render_template('create_recipe.html')

@app.route("/previous-recipes", methods=['GET', 'POST'])
def previous_recipes():
    recipes = main("lookup")

    if request.method == 'POST':
        data = request.get_json()
        recipe_id = data.get('recipeId')

        show_recipe = main("lookup", recipe_id)
        return jsonify({"show_recipe": show_recipe})
    
    return render_template('previous_recipes.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
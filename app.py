from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/create-recipe")
def create_recipe():
    return render_template('create_recipe.html')

@app.route("/previous-recipes")
def previous_recipes():
    return render_template('previous_recipes.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
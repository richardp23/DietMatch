import sqlite3


def create_tables():
    try:
        with sqlite3.connect('recipes.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS original_recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                recipe_link TEXT NOT NULL
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS alt_recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_recipe_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                FOREIGN KEY (original_recipe_id)
                REFERENCES original_recipes(id)
            )
            ''')
        print("Tables created successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def check_existing_recipe(cursor, table, **conditions):
    query = (
        f"SELECT id FROM {table} WHERE " +
        " AND ".join(f"{key} = ?" for key in conditions)
    )
    cursor.execute(query, tuple(conditions.values()))
    return cursor.fetchone()


def store_recipe(table, **data):
    try:
        with sqlite3.connect('recipes.db') as connection:
            cursor = connection.cursor()

            existing_recipe = check_existing_recipe(cursor, table, **data)
            if existing_recipe:
                print(f"Recipe already exists in the {table} table.")
                return existing_recipe[0]

            columns = ', '.join(data.keys())
            placeholders = ', '.join('?' * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, tuple(data.values()))
            print(f"Inserted recipe into {table} with ID: {cursor.lastrowid}")
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None


def store_original_recipe(name, ingredients, recipe_link):
    ingredients_str = ', '.join(ingredients)
    return store_recipe('original_recipes',
                        name=name,
                        ingredients=ingredients_str,
                        recipe_link=recipe_link)


def store_alt_recipe(original_recipe_id, name, ingredients, instructions):
    ingredients_str = ', '.join(ingredients)
    return store_recipe('alt_recipes',
                        original_recipe_id=original_recipe_id,
                        name=name, ingredients=ingredients_str,
                        instructions=instructions)


def lookup_prev_recipe():
    try:
        with sqlite3.connect('recipes.db') as connection:
            cursor = connection.cursor()

            cursor.execute('''
            SELECT o.id, o.name AS original_name, a.name AS alt_name
            FROM original_recipes o
            LEFT JOIN alt_recipes a ON o.id = a.original_recipe_id
            ''')
            recipes = cursor.fetchall()

        if recipes:
            print("\nPreviously made recipes:")
            for recipe in recipes:
                original_id, original_name, alt_name = recipe
                alt_name = (
                    alt_name if alt_name else "No alternative recipe found"
                )
                print((
                    f"{original_id}. {original_name} "
                    f"(Alternative Recipe: {alt_name})"
                    ))
            return True, recipes
        else:
            print("\nNo recipes found.")
            return False, None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False, None


def select_recipe(recipe_id):
    try:
        with sqlite3.connect('recipes.db') as connection:
            cursor = connection.cursor()

            cursor.execute('''
            SELECT name, ingredients, recipe_link
            FROM original_recipes
            WHERE id = ?
            ''', (recipe_id,))
            original_recipe = cursor.fetchone()

            cursor.execute('''
            SELECT name, ingredients, instructions
            FROM alt_recipes
            WHERE original_recipe_id = ?
            ''', (recipe_id,))
            alt_recipe = cursor.fetchone()

        if original_recipe:
            print("\nOriginal Recipe:")
            print(f"Name: {original_recipe[0]}")
            print(f"Ingredients: {original_recipe[1]}")
            print(f"Link: {original_recipe[2]}")
        else:
            print("\nOriginal recipe not found.")

        if alt_recipe:
            return (
                f"\nAlternative Recipe:"
                f"\nName: {alt_recipe[0]}"
                f"\nIngredients: {alt_recipe[1]}"
                f"\nInstructions: {alt_recipe[2]}"
            )
        else:
            print("\nAlternative recipe not found.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def reset_database():
    try:
        with sqlite3.connect('recipes.db') as connection:
            cursor = connection.cursor()
            cursor.execute('DROP TABLE IF EXISTS alt_recipes')
            cursor.execute('DROP TABLE IF EXISTS original_recipes')
            create_tables()
        print("Database reset successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


# Main execution
if __name__ == "__main__":
    create_tables()

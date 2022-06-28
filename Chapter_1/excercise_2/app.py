from flask import Flask, jsonify, request
from http import HTTPStatus


# Create flask instance
app = Flask(__name__)

# Recipes list
recipes = [
    {
        'id': 1,
        'name': 'Egg Salad',
        'description': 'This is a lovely egg salad recipe'
    },
    {
        'id':2,
        'name': 'Tomato Pasta',
        'description': 'This is a lovely tomato pasta recipe'
    }
]

@app.route('/recipes', methods=['GET'])
def index():
    return jsonify({'data': recipes})


@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)

    if recipe:
        return jsonify(recipe)
    
    return jsonify({'message': 'recipe not found'}, HTTPStatus.NOT_FOUND)


if __name__ == '__main__':
    app.run(debug=True)
from flask import Blueprint, jsonify, request
from app.schemas import food_schema, foods_schema
from app.models import Food, db
from sqlalchemy.sql.expression import func


foods_bp = Blueprint('foods',__name__,url_prefix='/api/foods')

#get all Foods
@foods_bp.route('/',methods=['GET'])
def get_orders():
    foods = Food.query.all()
    return jsonify(foods_schema.dump(foods))

#Get specific Food
@foods_bp.route('/<int:id>', methods=['GET'])
def get_food(id):
    food = Food.query.get_or_404(id)
    return jsonify(food_schema.dump(food))

# Get 4 random popular recipes
@foods_bp.route('/popular', methods=['GET'])
def get_popular_foods():
    try:
        # Fetch 4 random recipes
        popular_foods = Food.query.order_by(func.random()).limit(4).all()
        return jsonify(foods_schema.dump(popular_foods)), 200
    except Exception as e:
        print(f"Error fetching popular recipes: {e}")
        return jsonify({'error': 'Unable to fetch popular recipes'}), 500


#create a new food recipe
@foods_bp.route('/', methods=['POST'])
def create_food():
    data = request.get_json()
    
    if not data:
        return jsonify({'message':'No data provided'}), 400
    
    #validte data using schema
    errors = food_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    try:
        new_food = Food(**data)
        db.session.add(new_food)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 # Return any database error

    return jsonify(food_schema.dump(new_food)), 201

#update a specific food recipe
@foods_bp.route('/<int:id>', methods=['PUT'])
def update_food(id):
    food = Food.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({'message':'No data provided'}), 400
    
    errors = food_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    # Update fields only if they are present in the request
    if 'name' in data:
        food.name = data['name']
    if 'category' in data:
        food.category = data['category']
    if 'ingredients' in data:
        food.ingredients = data['ingredients']
    if 'instructions' in data:
        food.instructions = data['instructions']

    db.session.commit()

    return jsonify(food_schema.dump(food))

#delete a specific recipe
@foods_bp.route('/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    food = Food.query.get_or_404(id)

    db.session.delete(food)
    db.session.commit()

    return jsonify({'message': 'Recipe deleted successfully'}), 200

# Fetch foods by category
@foods_bp.route('/category/<string:category>', methods=['GET'])
def get_foods_by_category(category):
    foods = Food.query.filter_by(category=category).all()
    if not foods:
        return jsonify({'message': 'No foods found in this category'}), 404
    return jsonify(foods_schema.dump(foods)), 200

#search for foods according to the ingedients
@foods_bp.route('/search', methods=['POST'])
def search_foods():
    data = request.get_json()
    
    if not data or 'ingredients' not in data or 'category' not in data:
        return jsonify({'message': 'Please provide ingredients and a category'}), 400

    user_ingredients = set(data['ingredients'])  # Convert list to a set for easy comparison
    category = data['category']

    # Find foods in the given category
    foods = Food.query.filter_by(category=category).all()

    # Filter foods that can be made with the given ingredients
    possible_foods = []
    for food in foods:
        if set(food.ingredients).issubset(user_ingredients):  
            possible_foods.append(food)

    if not possible_foods:
        return jsonify({'message': 'No matching foods found'}), 404

    # Serialize the response
    return jsonify({'possible_foods': foods_schema.dump(possible_foods)})

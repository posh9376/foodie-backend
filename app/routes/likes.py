from flask import Blueprint, jsonify
from app.models import Like,Food,User,db
from flask_jwt_extended import jwt_required, get_jwt_identity

likes_bp = Blueprint('likes', __name__, url_prefix='/api/foods')

#liking a post
@likes_bp.route('/<int:food_id>/like', methods=['POST'])
@jwt_required()
def like_food(food_id):
    user_id = get_jwt_identity()
    food = Food.query.get_or_404(food_id)

    #check if the user already liked the post
    existing_like = Like.query.filter_by(user_id=int(user_id), food_id=food_id).first()
    if existing_like:
        return jsonify({'message': 'You aready liked the post'}),400
    
    like = Like(user_id = int(user_id), food_id = food_id)
    db.session.add(like)
    db.session.commit()
    return jsonify({'message': 'post Liked'}),201


#unliking a post
@likes_bp.route('/<int:food_id>/unlike', methods=['DELETE'])
@jwt_required()
def unlike_food(food_id):
    user_id = get_jwt_identity()
    like = Like.query.filter_by(food_id = food_id, user_id = int(user_id)).first()
    if not like:
        return jsonify({'message': 'No like found'})
    
    db.session.delete(like)
    db.session.commit()
    return jsonify({'message': 'Recipe unliked successfully'}), 200

#get number of likes a recipe has
@likes_bp.route('/<int:food_id>/likes', methods=['GET'])
def get_likes(food_id):
    likes_count = Like.query.filter_by(food_id=food_id).count()
    return jsonify({'likes': likes_count})
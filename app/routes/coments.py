from flask import Blueprint, request, jsonify
from app.schemas import comments_schema, comment_schema
from app.models import Comment, db, Food, User
from flask_jwt_extended import jwt_required, get_jwt_identity


comments_bp = Blueprint('comments', __name__, url_prefix ='/api')
#get all comments
@comments_bp.route('/<int:food_id>/comments', methods=['GET'])
def get_comments(food_id):
    comments = Comment.query.filter_by(food_id=food_id).all()
    return jsonify(comments_schema.dump(comments)),200

#create a new comment according to user
@comments_bp.route('/<int:food_id>/comment', methods=['POST'])
@jwt_required()
def create_comment(food_id):
    data = request.get_json()
    current_user = get_jwt_identity()
    comment = data.get('comment')

    if not data:
        return jsonify({'message':'No data provided'}), 400
    
    # Check that food and user exist
    food = Food.query.get_or_404(food_id)
    user = User.query.get_or_404(current_user)

    #create new comment
    new_comment = Comment(food_id = food_id, user_id = current_user, comment= comment)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify(comment_schema.dump(new_comment)),201


#delete a comment
#only the one who posted can delete the comment
@comments_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def comment_delete(comment_id):
    current_user = get_jwt_identity()
    comment = Comment.query.get_or_404(comment_id)

    if comment.user_id != int(current_user):
        return jsonify ({'error': 'Unauthorised access'}), 403
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'comment deleted successfully'}), 200  
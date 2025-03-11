from flask import Blueprint, jsonify, request
from app.schemas import user_schema
from app.models import User, db
from flask_jwt_extended import create_access_token


user_bp = Blueprint('user', __name__, url_prefix='/api/user')

from flask import request, jsonify
from werkzeug.security import generate_password_hash
from app.models import User, db  # Ensure correct imports
from flask_jwt_extended import create_access_token

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate required fields
    required_fields = ['username', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    # Create new user instance
    new_user = User(
        username=data['username'],
        email=data['email']
    )
    new_user.set_password(data['password'])  # Use set_password methodto hash the password

    # Save user to database
    db.session.add(new_user)
    db.session.commit()

    # Generate access token
    access_token = create_access_token(identity=str(new_user.id))

    return jsonify({
        'message': 'User added successfully',
        'token': access_token,
        'user': user_schema.dump(new_user)
    }), 201



@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate input
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400

    # Find user by email
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):  # Ensure method exists
        return jsonify({'error': 'Invalid email or password'}), 401

    # Generate JWT token
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token
    }), 200

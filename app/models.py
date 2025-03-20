from .extensions import db
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from werkzeug.security import generate_password_hash, check_password_hash

class Food(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(ARRAY(db.String), nullable=False)
    instructions = db.Column(JSONB, nullable=False)
    image_url =db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    #relationship
    user = db.relationship('User', back_populates = 'foods', lazy=True)
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    #relationship
    foods = db.relationship('Food', back_populates = 'user',lazy =True)

    def set_password(self, password):
        """Hash and store the user's password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hash"""
        return check_password_hash(self.password_hash, password)
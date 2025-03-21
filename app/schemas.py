from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)


class FoodSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    ingredients = fields.List(fields.Str(), required=True)
    instructions = fields.List(fields.Dict(), required=True)  # Assuming JSON steps
    image_url = fields.Str(required=True)
    user_id = fields.Int(required=True)
    username = fields.Method('get_username')

    def get_username(self, obj):
        return obj.user.username if obj.user else None


class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    food_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    comment = fields.Str(required=True)
    username = fields.Method('get_username')
    created_at = fields.DateTime(dump_only=True)

    def get_username(self, obj):
        return obj.user.username if obj.user else None

class LikeSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    food_id = fields.Int(required=True)


# Schema instances for easy use
user_schema = UserSchema()
food_schema = FoodSchema()
foods_schema = FoodSchema(many=True)
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
like_schema = LikeSchema()
likes_schema =LikeSchema(many=True)

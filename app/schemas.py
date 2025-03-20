from marshmallow import Schema, fields

class FoodSchema(Schema):
    id = fields.Int(dump_only=True)  # Only returned, not required in input
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    ingredients = fields.List(fields.Str(), required=True)  # Validate list of strings
    instructions = fields.List(fields.Dict(), required=True)  # Validate list of steps in JSON format
    image_url = fields.Str(required=True)
    user_id = fields.Int(required=True)
    #getting the username from the db
    username = fields.Method('get_username')

    #define the method
    def get_username(self, obj):
        return obj.user.username if obj.user else None




class UsersSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)


#instances
food_schema = FoodSchema()
foods_schema = FoodSchema(many = True)
user_schema = UsersSchema()

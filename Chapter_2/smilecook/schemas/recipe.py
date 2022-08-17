from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.user import UserSchema
from schemas.pagination import PaginationSchema
from flask import url_for

def validate_num_of_servings(num):
        if num < 1:
            raise ValidationError('Number of servings must be greater than 0.')
        if num > 50:
            raise ValidationError('Number of servings must not be greater than 50.')


class RecipeSchema(Schema):
    class Meta:
            ordered = True
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    description = fields.String(validate= [validate.Length(max=200)])
    num_of_servings =  fields.Integer(validate=validate_num_of_servings)
    cook_time = fields.Integer()
    directions = fields.String(required=True, validate=[validate.Length(max=1000)])
    is_publish = fields.Boolean(dump_only=True)
    recipe_cover_url = fields.Method(serialize='dump_cover_url')
                                                                          # Only show the user's ID and username
    author =  fields.Nested(UserSchema, attribute='user', dump_only=True, exclude=['email'])
    created_at = fields.DateTime(dump_only =True)
    updated_at = fields.DateTime(dump_only =True)

    # Another way using a decorator of marshmallow to validate data
    @validates('cook_time')
    def validate_cook_time(self, value):
        if value < 1:
            raise ValidationError('Cook time must be greater than 0.')
        if value > 300:
            raise ValidationError('Cook time must not be greater than 300.')
    
    # Can be deleted after, in comments because of learning purposes
    # @post_dump(pass_many=True)
    # def wrap(self, data, many, **kwargs):
    #     if many:
    #         return {'data': data}
    #     return data



    def dump_cover_url(self, user):
        """ Returns the cover_url of the uploaded recipe cover """
        if user.cover_image:
            return url_for('static', filename='images/recipes/{}'.format(user.cover_image), _external=True)
        else:
            return url_for('static', filename='images/assets/default-cover.jpg', _external=True)


class RecipePaginationSchema(PaginationSchema):
    data = fields.Nested(RecipeSchema, attribute='items', many=True)
    


   



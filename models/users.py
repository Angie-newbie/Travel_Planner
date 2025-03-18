from init import db, ma
from marshmallow_sqlalchemy import fields
from marshmallow.fields import Email

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'travel'} 


    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(200), nullable = False, unique = True)

    user_trips = db.relationship('Trip', back_populates = 'user')
                        
class UserSchema(ma.Schema):
    email = Email(required=True)
    user_trips = fields.Nested('TripSchema', many=True, only=['location', 'total_expense']) 

    class Meta:
        include_fk = True 
        fields = ('id', 'name', 'email', 'user_trips')

one_user = UserSchema()
many_users = UserSchema(many = True)
user_without_id = UserSchema(exclude=['id'])

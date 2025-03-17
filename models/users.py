from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'academy'} 


    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(200), nullable = False, unique = True)

                        
class UserSchema(ma.Schema):
    email = Email(required=True)

    class Meta:
        fields = ('id', 'name', 'email')

one_user = UserSchema()
many_users = UserSchema(many = True)

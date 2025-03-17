from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from models.users import User, one_user, many_users, user_without_id

users_bp = Blueprint('users', __name__)

# Read all 
@users_bp.route('/users', methods=['GET'])
def get_all_users():
    stmt = db.select(User).order_by(User.name.desc())
    users = db.session.scalars(stmt)
    return many_users.dump(users)

# Read one
@users_bp.route('/users/<int:user_id>')
def get_one_user(user_id):
    stmt = db.select(User).filter_by(id = user_id)
    user = db.session.scalar(stmt)
    if user:
        return one_user.dump(user)
    else:
        return {'error': f'Sorry, user with id {user_id} does not exits'}, 404
    
# Update - PUT 
@users_bp.route('/users/<int:user_id>', methods = ['PUT', 'PATCH'])
def update_user(user_id):
    try:
        
        # Fetch user by id
        stmt = db.select(User).filter_by(id = user_id)
        user = db.session.scalar(stmt)
        if user:
            # Pre-check if 'id' is present in the incoming data and remove it
            incoming_data = request.json
            if 'id' in incoming_data:
                del incoming_data['id']  # Remove 'id' from the data

            # Get incoming request body
            data = user_without_id.load(request.json)

            
            # update the attribute of the user with the incoming data
            user.name = data.get('name') or user.name
            user.email = data.get('email') or user.email

            db.session.commit()
            return one_user.dump(user)
        else:
            return {'error': f'User with id {user_id} does not exist'}, 404 
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return{"error": "email address already in use"}, 409
        else:
            return{"error": err._message()}, 400
    

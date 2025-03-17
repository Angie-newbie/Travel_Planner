from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from models.users import User, one_user, many_users, user_without_id

users_bp = Blueprint('users', __name__)

# Helper function to fetch all users
def get_all_users_from_db():
    stmt = db.select(User).order_by(User.name.desc())
    return db.session.scalars(stmt)

# Helper function to fetch user by id
def get_user_by_id(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    return db.session.scalar(stmt)

# Helper function to handle integrity errors
def handle_integrity_error(err):
    if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
        return {"error": "Email address already in use."}, 409
    else:
        return {"error": err._message()}, 400

# Helper function to check if user email exists (excluding the current user)
def is_email_exists(email, exclude_id=None):
    existing_user = db.session.query(User).filter_by(email=email).first()
    return existing_user and (existing_user.id != exclude_id if exclude_id else True)

# Helper function to validate required fields in data
def validate_required_fields(data, fields):
    for field in fields:
        if not data.get(field):
            return {"error": f"'{field}' field is required"}, 400
    return None

# Read all 
@users_bp.route('/users', methods=['GET'])
def get_all_users():
    users = get_all_users_from_db()
    return many_users.dump(users)

# Read one
@users_bp.route('/users/<int:user_id>')
def get_one_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return one_user.dump(user)
    else:
        return {'error': f'Sorry, user with id {user_id} does not exits'}, 404
    
# Update - PUT 
@users_bp.route('/users/<int:user_id>', methods = ['PUT', 'PATCH'])
def update_user(user_id):
    try:
        
        # Fetch user by id
        user = get_user_by_id(user_id)
        if user:
            # Pre-check if 'id' is present in the incoming data and remove it
            incoming_data = request.json
            incoming_data.pop('id', None)  # Remove 'id' from the data

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
        return handle_integrity_error(err)

        
# Create - POST
@users_bp.route('/users', methods = ['POST'])
def create_user():
    try:
        # Get incoming request body(json)
        data = user_without_id.load(request.json)

        # Validate that 'name' and 'email' are provided in the request
        validation_error = validate_required_fields(data, ['name', 'email'])
        if validation_error:
            return validation_error
        
        if is_email_exists(data.get('email')):
            return {"error": "Email address already exists."}, 409
        
        new_user = User(
            name = data.get('name'),
            email = data.get('email')
        )
        # Add the instance to the db session
        db.session.add(new_user)
        # Commit the session
        db.session.commit()
        # Return the new user instance 
        return one_user.dump(new_user), 201
    except IntegrityError as err:
        return handle_integrity_error(err)

# Delete - DELETE
@users_bp.route('/users/<int:user_id>', methods = ['DELETE'])
def delete_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': f'User with id {user_id} has been deleted successfully'}, 200
    else:
        return {'error': f'User with id {user_id} does not exist'}, 404

    

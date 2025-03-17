from flask import Blueprint, request
from init import db
from models.users import User, one_user, many_users

users_bp = Blueprint('users', __name__)

# Read all - GET /students
@users_bp.route('/users')
def get_all_users():
    stmt = db.select(User).order_by(User.name.desc())
    users = db.session.scalars(stmt)
    return many_users.dump(users)
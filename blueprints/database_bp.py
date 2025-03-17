from flask import Blueprint
from init import db
from datetime import date
from models.users import User

db_bp = Blueprint('db', __name__)

@db_bp.cli.command('init')
def create_tables():
    db.drop_all()
    db.create_all()
    print('Tables Created')

@db_bp.cli.command('seed')
def seed_tables():
    users = [
        User(
            name = 'Mary Jones',
            email = 'mary.jons@gmail.com',
        ),
        User( 
            name = 'John Smith',
            email = 'john.smith@outlook.com'
        )
    ]

    db.session.add_all(users)
    db.session.commit()
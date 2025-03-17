from flask import Blueprint
from init import db
from datetime import date
from models.users import User
from models.categories import Category
from models.trips import Trip

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

    cateogories = [
        Category(
            name = 'Food',
        ),
        Category( 
            name = 'Shopping',
        )
    ]
    
    trips = [
        Trip(
            location = 'Japan',
            arrival_date = 
            departure_date = 
            user_id = 
            total_expense
        ),
        Trip( 
            name = 'Shopping',
        )
    ]

    db.session.add_all(users)
    db.session.add_all(cateogories)
    db.session.add_all(trips)
    db.session.commit()
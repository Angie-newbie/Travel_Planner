from flask import Blueprint
from init import db
from datetime import date
from models.users import User
from models.categories import Category
from models.trips import Trip
from models.expenses import Expense

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

    categories = [
        Category(
            name = 'Food',
        ),
        Category( 
            name = 'Shopping',
        )
    ]
    
    db.session.add_all(categories)
    db.session.commit() 
    trips = [
        Trip(
            location = 'Japan',
            arrival_date = date(2025, 4, 8),
            departure_date = date(2025, 4, 20),
            user_id=1
        ),
        Trip( 
            location = 'Korea',
            arrival_date = date(2025, 3, 26),
            departure_date = date(2025, 4, 8),
            user_id=1
        )
    ]

    expenses = [
        Expense(
            amount = 100, 
            description = "Ramen",
            trip=trips[0], 
            category=categories[0]
        ),
        Expense( 
            amount = 100, 
            description = "Bag"
        )
    ]


    db.session.add_all(trips)
    db.session.add_all(expenses)
    db.session.commit()
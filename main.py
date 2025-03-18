from flask import Flask
from init import db, ma
from models.users import User
import os
from blueprints.database_bp import db_bp
from blueprints.users_bp import users_bp
from blueprints.categories_bp import categories_bp
from blueprints.trips_bp import trips_bp
from blueprints.expenses_bp import expenses_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://lms_dev:123456@localhost:5432/travelplanner_db'


    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(expenses_bp)

    return app

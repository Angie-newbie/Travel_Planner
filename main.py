from flask import Flask
from init import db, ma
import os
from dotenv import load_dotenv
from blueprints.database_bp import db_bp
from blueprints.users_bp import users_bp
from blueprints.categories_bp import categories_bp
from blueprints.trips_bp import trips_bp
from blueprints.expenses_bp import expenses_bp

def create_app():
    app = Flask(__name__)

    load_dotenv(override=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(expenses_bp)

    return app

from flask import Flask
from init import db, ma
import os

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lms_dev:123456@localhost:5432/lms_db'
    

    db.init_app(app)
    ma.init_app(app)

    return app

from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from models.categories import Category, one_category, many_categories, category_without_id

categories_bp = Blueprint('categories', __name__)

# Read all 
@categories_bp.route('/categories', methods=['GET'])
def get_all_categories():
    stmt = db.select(Category).order_by(Category.name.desc())
    categories = db.session.scalars(stmt)
    return many_categories.dump(categories)

# Read one
@categories_bp.route('/categories/<int:category_id>')
def get_one_category(category_id):
    stmt = db.select(Category).filter_by(id = category_id)
    category = db.session.scalar(stmt)
    if category:
        return one_category.dump(category)
    else:
        return {'error': f'Sorry, category with id {category_id} does not exits'}, 404
    
# Update - PUT 
@categories_bp.route('/categories/<int:category_id>', methods = ['PUT', 'PATCH'])
def update_category(category_id):
    try:
        
        # Fetch category by id
        stmt = db.select(Category).filter_by(id = category_id)
        category = db.session.scalar(stmt)
        if category:
            # Pre-check if 'id' is present in the incoming data and remove it
            incoming_data = request.json
            if 'id' in incoming_data:
                del incoming_data['id']  # Remove 'id' from the data

            # Get incoming request body
            data = category_without_id.load(request.json)

            # update the attribute of the category with the incoming data
            category.name = data.get('name') or category.name

            db.session.commit()
            return one_category.dump(category)
        else:
            return {'error': f'Category with id {category_id} does not exist'}, 404 
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return{"error": "categpry name already in use"}, 409
        else:
            return{"error": err._message()}, 400
        
# Create - POST
@categories_bp.route('/categories', methods = ['POST'])
def create_category():
    try:
        # Get incoming request body(json)
        data = category_without_id.load(request.json)

        if not data.get('name'):
            return {"error": "'name' field is required"}, 400
        
        new_category = Category(
            name = data.get('name'),
        )

        # Add the instance to the db session
        db.session.add(new_category)
        # Commit the session
        db.session.commit()
        # Return the new category instance 
        return one_category.dump(new_category), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: 
            # unique violation
            return {"error": "category name already in use"}, 409
        else:
            return{"error": err._message()}, 400

# Delete - DELETE
@categories_bp.route('/categories/<int:category_id>', methods = ['DELETE'])
def delete_category(category_id):
    stmt = db.select(Category).filter_by(id = category_id)
    category = db.session.scalar(stmt)
    if category:
        db.session.delete(category)
        db.session.commit()
        return {'message': f'Category with id {category_id} has been deleted successfully'}, 200
    else:
        return {'error': f'Category with id {category_id} does not exist'}, 404

    

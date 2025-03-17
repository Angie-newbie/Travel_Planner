from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from models.categories import Category, one_category, many_categories, category_without_id

categories_bp = Blueprint('categories', __name__)

# Helper function to fetch all categories
def get_all_categories_from_db():
    stmt = db.select(Category).order_by(Category.name.desc())
    return db.session.scalars(stmt)

# Helper function to fetch category by id
def get_category_by_id(category_id):
    stmt = db.select(Category).filter_by(id=category_id)
    return db.session.scalar(stmt)

# Helper function to check if category name exists (excluding the current category)
def is_category_name_exists(name, exclude_id=None):
    existing_category = db.session.query(Category).filter_by(name=name).first()
    return existing_category and (existing_category.id != exclude_id if exclude_id else True)

# Helper function to handle integrity errors
def handle_integrity_error(err):
    if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
        return {"error": "Category name already in use"}, 409
    else:
        return {"error": err._message()}, 400

# Read all 
@categories_bp.route('/categories', methods=['GET'])
def get_all_categories():
    categories = get_all_categories_from_db()
    return many_categories.dump(categories)

# Read one
@categories_bp.route('/categories/<int:category_id>')
def get_one_category(category_id):
    category = get_category_by_id(category_id)
    if category:
        return one_category.dump(category)
    else:
        return {'error': f'Sorry, category with id {category_id} does not exits'}, 404
    
# Update - PUT 
@categories_bp.route('/categories/<int:category_id>', methods = ['PUT', 'PATCH'])
def update_category(category_id):
    try:
        
        # Fetch category by id
        category = get_category_by_id(category_id)
        if category:
            # Pre-check if 'id' is present in the incoming data and remove it
            incoming_data = request.json
            incoming_data.pop('id', None) 

            # Get incoming request body
            data = category_without_id.load(request.json)

            # Check if the new category name already exists (to enforce uniqueness)
            if is_category_name_exists(data.get('name'), exclude_id=category.id):
                return {"error": "Category name already in use."}, 409

            # update the attribute of the category with the incoming data
            category.name = data.get('name') or category.name

            db.session.commit()
            return one_category.dump(category)
        else:
            return {'error': f'Category with id {category_id} does not exist'}, 404 
    except IntegrityError as err:
        return handle_integrity_error(err)
        
# Create - POST
@categories_bp.route('/categories', methods = ['POST'])
def create_category():
    try:
        # Get incoming request body(json)
        data = category_without_id.load(request.json)

        if not data.get('name'):
            return {"error": "'name' field is required"}, 400
        
        # Pre-check if the category name already exists
        if is_category_name_exists(data.get('name')):
            return {"error": "Category name already exists."}, 409
        
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
        return handle_integrity_error(err)

# Delete - DELETE
@categories_bp.route('/categories/<int:category_id>', methods = ['DELETE'])
def delete_category(category_id):
    category = get_category_by_id(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return {'message': f'Category with id {category_id} has been deleted successfully'}, 200
    else:
        return {'error': f'Category with id {category_id} does not exist'}, 404

    

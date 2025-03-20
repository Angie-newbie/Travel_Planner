from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from models.trips import Trip
from models.categories import Category 
from models.expenses import Expense, one_expense, many_expenses, expense_without_id

expenses_bp = Blueprint('expenses', __name__)

# Helper function to fetch expenses
def get_expense(expense_id=None):
    stmt = db.select(Expense).order_by(Expense.amount.desc()) if expense_id is None else db.select(Expense).filter_by(id=expense_id)
    return db.session.scalars(stmt) if expense_id is None else db.session.scalar(stmt)

# Helper function to handle integrity errors
def handle_integrity_error(err):
        return {"error": err._message()}, 400

# Helper function for validating required fields
def validate_required_fields(data, required_fields):
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return {"error": f"Missing required fields: {', '.join(missing_fields)}"}, 400
    return None

# Read all 
@expenses_bp.route('/expenses', methods=['GET'])
def get_all_expenses():
    return many_expenses.dump(get_expense())

# Read one
@expenses_bp.route('/expenses/<int:expense_id>')
def get_one_expense(expense_id):
    expense = get_expense(expense_id)
    return one_expense.dump(expense) if expense else ({'error': f'Expense with id {expense_id} not found'}, 404)
    
# Update - PUT 
@expenses_bp.route('/expenses/<int:expense_id>', methods = ['PUT', 'PATCH'])
def update_expense(expense_id):
    try:
        
        # Fetch expense by id
        expense = get_expense(expense_id)
        if not expense:
            return {'error': f'Expense with id {expense_id} not found'}, 404

        # Get incoming request body
        data = expense_without_id.load(request.json)
        data.pop('id', None)

        # Update only provided fields
        for key, value in data.items():
            setattr(expense, key, value)

        db.session.commit()
        return one_expense.dump(expense)
    except IntegrityError as err:
        return handle_integrity_error(err)
        
# Create - POST
@expenses_bp.route('/expenses', methods = ['POST'])
def create_expense():
    try:
        # Get incoming request body(json)
        data = expense_without_id.load(request.json)

        # Validate required fields
        required_fields = ['amount', 'category_id', 'description', 'trip_id']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return validation_error

        # Create and commit new expense
        new_expense = Expense(**data)
        db.session.add(new_expense)
        db.session.commit()

        # Add the instance to the db session
        db.session.add(new_expense)
        # Commit the session
        db.session.commit()
        # Return the new expense instance 
        return one_expense.dump(new_expense), 201
    
    except ValidationError as err:
        return {"error": err.messages}, 400

    except IntegrityError as err:
        return handle_integrity_error(err)

# Delete - DELETE
@expenses_bp.route('/expenses/<int:expense_id>', methods = ['DELETE'])
def delete_expense(expense_id):
    expense = get_expense(expense_id)
    if not expense:
        return {'error': f'Expense with id {expense_id} not found'}, 404
    db.session.delete(expense)
    db.session.commit()
    return {'message': f'Expenses with id {expense_id} has been deleted successfully'}, 200


    

from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from models.expenses import Expense, one_expense, many_expenses, expense_without_id

expenses_bp = Blueprint('expenses', __name__)

# Helper function to fetch all expenses
def get_all_expenses_from_db():
    stmt = db.select(Expense).order_by(Expense.name.desc())
    return db.session.scalars(stmt)

# Helper function to fetch expense by id
def get_expense_by_id(expense_id):
    stmt = db.select(Expense).filter_by(id=expense_id)
    return db.session.scalar(stmt)

# Helper function to check if expense name exists (excluding the current expense)
def is_expense_name_exists(name, exclude_id=None):
    existing_expense = db.session.query(Expense).filter_by(name=name).first()
    return existing_expense and (existing_expense.id != exclude_id if exclude_id else True)

# Helper function to handle integrity errors
def handle_integrity_error(err):
    if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
        return {"error": "Expenses name already in use"}, 409
    else:
        return {"error": err._message()}, 400

# Read all 
@expenses_bp.route('/expenses', methods=['GET'])
def get_all_expenses():
    expenses = get_all_expenses_from_db()
    return many_expenses.dump(expenses)

# Read one
@expenses_bp.route('/expenses/<int:expense_id>')
def get_one_expense(expense_id):
    expense = get_expense_by_id(expense_id)
    if expense:
        return one_expense.dump(expense)
    else:
        return {'error': f'Sorry, expense with id {expense_id} does not exits'}, 404
    
# Update - PUT 
@expenses_bp.route('/expenses/<int:expense_id>', methods = ['PUT', 'PATCH'])
def update_expense(expense_id):
    try:
        
        # Fetch expense by id
        expense = get_expense_by_id(expense_id)
        if expense:
            # Pre-check if 'id' is present in the incoming data and remove it
            incoming_data = request.json
            incoming_data.pop('id', None) 

            # Get incoming request body
            data = expense_without_id.load(request.json)

            # Check if the new expense name already exists (to enforce uniqueness)
            if is_expense_name_exists(data.get('name'), exclude_id=expense.id):
                return {"error": "Expenses name already in use."}, 409

            # update the attribute of the expense with the incoming data
            expense.name = data.get('name') or expense.name

            db.session.commit()
            return one_expense.dump(expense)
        else:
            return {'error': f'Expenses with id {expense_id} does not exist'}, 404 
    except IntegrityError as err:
        return handle_integrity_error(err)
        
# Create - POST
@expenses_bp.route('/expenses', methods = ['POST'])
def create_expense():
    try:
        # Get incoming request body(json)
        data = expense_without_id.load(request.json)

        if not data.get('name'):
            return {"error": "'name' field is required"}, 400
        
        # Pre-check if the expense name already exists
        if is_expense_name_exists(data.get('name')):
            return {"error": "Expenses name already exists."}, 409
        
        new_expense = Expense(
            name = data.get('name'),
        )

        # Add the instance to the db session
        db.session.add(new_expense)
        # Commit the session
        db.session.commit()
        # Return the new expense instance 
        return one_expense.dump(new_expense), 201
    except IntegrityError as err:
        return handle_integrity_error(err)

# Delete - DELETE
@expenses_bp.route('/expenses/<int:expense_id>', methods = ['DELETE'])
def delete_expense(expense_id):
    expense = get_expense_by_id(expense_id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
        return {'message': f'Expenses with id {expense_id} has been deleted successfully'}, 200
    else:
        return {'error': f'Expenses with id {expense_id} does not exist'}, 404

    

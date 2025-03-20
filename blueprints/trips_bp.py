from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from init import db
from models.users import User
from models.trips import Trip, many_trips, one_trip, trip_without_id

trips_bp = Blueprint('trips', __name__)

# Helper function to fetch trip by ID
def get_trip_by_id(trip_id):
    return db.session.scalar(db.select(Trip).filter_by(id=trip_id))

# Helper function to validate user ID
def validate_user(user_id):
    if not User.query.get(user_id):
        return {"error": "Invalid user_id. User does not exist."}, 400

# Helper function to parse and validate dates
def parse_date(date_str, field_name):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return {"error": f"Invalid date format for {field_name}. Use YYYY-MM-DD."}, 400

# Read all - GET /trips
@trips_bp.route('/trips')
def get_all_trips():
    trips = db.session.scalars(db.select(Trip).order_by(Trip.location.desc()))
    return many_trips.dump(trips)

# Read one - GET / trips/ <int:id>
@trips_bp.route('/trips/<int:trip_id>')
def get_one_trip(trip_id):
    trip = get_trip_by_id(trip_id)
    return one_trip.dump(trip) if trip else {"error": f"Trip with id {trip_id} does not exist"}, 404

# Create - POST / trips
@trips_bp.route('/trips', methods = ['POST'])
def create_trip():
    try:
        # Get incoming request body(json)
        data = trip_without_id.load(request.json)

        required_fields = ['location', 'arrival_date', 'departure_date', 'user_id']
        for field in required_fields:
            if not data.get(field):
                return {"error": f"'{field}' field is required"}, 400
        
        user_validation = validate_user(data['user_id'])
        if user_validation:
            return user_validation
        
        # Retrieve dates from data
        arrival_date = data.get('arrival_date')
        departure_date = data.get('departure_date')

        # Ensure arrival_date and departure_date are in the correct format
        if isinstance(arrival_date, str):
            try:
                arrival_date = datetime.strptime(arrival_date, '%Y-%m-%d').date()
            except ValueError:
                return {"error": "Invalid date format for arrival_date. Use YYYY-MM-DD."}, 400

        if isinstance(departure_date, str):
            try:
                departure_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
            except ValueError:
                return {"error": "Invalid date format for departure_date. Use YYYY-MM-DD."}, 400

        # Check that departure_date is after arrival_date
        if departure_date <= arrival_date:
            return {"error": "departure_date must be after arrival_date"}, 400
        
        new_trip = Trip(**data)
        # Add the instance to the db session
        db.session.add(new_trip)
        # Commit the session
        db.session.commit()
        # Return the new trip instance 
        return one_trip.dump(new_trip), 201
    except Exception as err:
            return{"error": str(err)}, 400


# Update - PUT / trips / <int:id>
@trips_bp.route('/trips/<int:trip_id>', methods = ['PUT', 'PATCH'])
def update_trip(trip_id):
    try:
        trip = get_trip_by_id(trip_id)
        if not trip:
            return {"error": f"Trip with id {trip_id} does not exist"}, 404
        
        data = trip_without_id.load(request.json)
        if 'user_id' in data:
            user_validation = validate_user(data['user_id'])
            if user_validation:
                return user_validation
        
        for key, value in data.items():
            setattr(trip, key, value)

            db.session.commit()
            return one_trip.dump(trip)

    except Exception as err:
            return{"error": str(err)}, 400

# Delete - DELETE/ trips / <int:id>
@trips_bp.route('/trips/<int:trip_id>', methods = ['DELETE'])
def delete_trip(trip_id):
    trip = get_trip_by_id(trip_id)
    if trip:
        db.session.delete(trip)
        db.session.commit()
        return {'message': f'Trip with id {trip_id} has been deleted successfully'}, 200
    else:
        return {'error': f'Trip with id {trip_id} does not exist'}, 404

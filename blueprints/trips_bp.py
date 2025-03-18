from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.users import User
from models.trips import Trip, many_trips, one_trip, trip_without_id

trips_bp = Blueprint('trips', __name__)

# Read all - GET /trips
@trips_bp.route('/trips')
def get_all_trips():
    stmt = db.select(Trip).order_by(Trip.location.desc())
    trips = db.session.scalars(stmt)
    return many_trips.dump(trips)


# Read one - GET / trips/ <int:id>
@trips_bp.route('/trips/<int:trip_id>')
def get_one_trip(trip_id):
    stmt = db.select(Trip).filter_by(id = trip_id)
    trip = db.session.scalar(stmt)
    if trip:
        return one_trip.dump(trip)
    else:
        return {'error': f'trip with id {trip_id} does not exits'}, 404

# Create - POST / trips
@trips_bp.route('/trips', methods = ['POST'])
def create_trip():
    try:
        # Get incoming request body(json)
        data = trip_without_id.load(request.json)

        new_trip = Trip(
            location = data.get('location'),
            departure_date = data.get('departure_date'),
            arrival_date = data.get('arrival_date'),
            user_id = data.get('user_id')
        )
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
        
        # Fetch trip by id
        stmt = db.select(Trip).filter_by(id = trip_id)
        trip = db.session.scalar(stmt)
        if trip:
            # Get incoming request body
            data = trip_without_id.load(request.json)
            # update the attribute of the trip with the incoming data
            trip.location = data.get('location') or trip.location
            trip.departure_date = data.get('departure_date') or trip.departure_date
            trip.arrival_date = data.get('arrival_date') or trip.arrival_date
            trip.user_id = data.get('user_id', trip.user_id)

            db.session.commit()
            return one_trip.dump(trip)
        else:
            return {'error': f'Trip with id {trip_id} does not exist'}, 404 
    except Exception as err:
            return{"error": str(err)}, 400

# Delete - DELETE/ trips / <int:id>
@trips_bp.route('/trips/<int:trip_id>', methods = ['DELETE'])
def delete_trip(trip_id):
    stmt = db.select(Trip).filter_by(id = trip_id)
    trip = db.session.scalar(stmt)
    if trip:
        db.session.delete(trip)
        db.session.commit()
        return {}, 204
    else:
        return {'error': f'Trip with id {trip_id} does not exist'}, 404

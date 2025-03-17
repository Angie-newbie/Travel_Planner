from init import db, ma
from marshmallow_sqlalchemy import fields
from marshmallow.fields import String
from sqlalchemy.orm import column_property
from sqlalchemy.sql import func



class Trip(db.Model):
    __tablename__ = 'trips'
    __table_args__ = {'schema': 'travel'} 

    id = db.Column(db.Integer, primary_key = True)

    location = db.Column(db.String(200), nullable = False)
    arrival_date = db.Column(db.Date, nullable = False)
    departure_date = db.Column(db.Date, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('travel.users.id'), nullable=False)
    
    total_expense = column_property(
        db.select(func.coalesce(func.sum(Expense.amount), 0))
        .where(Expense.trip_id == id)
        .scalar_subquery()
    )
                        
class TripSchema(ma.Schema):
    location = String(required=True)


    class Meta:
        fields = ('id', 'location', 'arrival_date', 'departure_date', 'user_id', 'total_expense')

one_trip = TripSchema()
many_trips = TripSchema(many = True)

trip_without_id = TripSchema(exclude=['id'])
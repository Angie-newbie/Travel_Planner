from init import db, ma
from marshmallow import Schema, fields
from sqlalchemy.orm import column_property
from sqlalchemy.sql import func
from models.expenses import Expense
from models.users import User



class Trip(db.Model):
    __tablename__ = 'trips'
    __table_args__ = {'schema': 'travel'} 

    id = db.Column(db.Integer, primary_key = True)

    location = db.Column(db.String(200), nullable = False)
    arrival_date = db.Column(db.Date, nullable = False)
    departure_date = db.Column(db.Date, nullable = False)

    # Define relationship with User
    user_id = db.Column(db.Integer, db.ForeignKey('travel.users.id'), nullable=False)
    user = db.relationship('User', back_populates='user_trips')
    # Define relationship with Expense
    expenses = db.relationship("Expense", back_populates="trip_location",lazy="dynamic")

    def total_expense(self):
        return db.session.query(db.func.sum(Expense.amount)).filter(Expense.trip_id == self.id).scalar() or 0
                        
class TripSchema(ma.Schema):
    id = fields.Int()
    location = fields.Str()
    arrival_date = fields.Date(error_messages={"invalid": "Invalid date format. Use YYYY-MM-DD."})
    departure_date = fields.Date(error_messages={"invalid": "Invalid date format. Use YYYY-MM-DD."})
    user_id = fields.Int()
    total_expense = fields.Method("get_total_expense")

    def get_total_expense(self, obj):
        return obj.total_expense()


    class Meta:
        fields = ('id', 'location', 'arrival_date', 'departure_date', 'user_id', 'total_expense')

one_trip = TripSchema()
many_trips = TripSchema(many = True)

trip_without_id = TripSchema(exclude=['id'])
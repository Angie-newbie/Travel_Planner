from init import db, ma
from marshmallow.fields import String, Length
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Expense(db.Model):
    __tablename__ = 'expenses'
    __table_args__ = {'schema': 'travel'} 


    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Float, nullable = False)
    description = db.Column(db.String(300))

    trip_id = db.Column(db.Integer, db.ForeignKey('travel.trips.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('travel.categories.id'), nullable=False)

    # Define relationships
    trip_location = db.relationship("Trip", back_populates="expenses", lazy="joined")
    category = db.relationship("Category", back_populates="expenses", lazy="joined")
                        
class ExpenseSchema(ma.Schema):

    amount = fields.Float(required=True)  # Include the amount field explicitly

    description = String(validate=Length(min=2, error="Description must be at least 2 characters"))

    # Foreign keys as integers
    # trip_id = fields.Int(required=True) 
    category_id = fields.Int(required=True) 

    # Nested fields
    # trip_location = fields.Nested('TripSchema', only=['location'])
    category = fields.Nested('CategorySchema', only=['name'])
    

     # Define a method to directly return the location
    trip_location = fields.Method("get_trip_location")

    def get_trip_location(self, obj):
        # Assuming the Expense model has a relationship to the Trip model
        return obj.trip_location.location if obj.trip_location else None

    class Meta:
        model = Expense
        fields = ('id', 'amount', 'description', 'trip_id', 'category_id', 'trip_location', 'category')

one_expense = ExpenseSchema()
many_expenses = ExpenseSchema(many = True)
expense_without_id = ExpenseSchema(exclude=['id'])
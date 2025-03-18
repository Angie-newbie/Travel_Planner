from init import db, ma
from marshmallow_sqlalchemy import fields
from marshmallow.fields import String, Length

class Expense(db.Model):
    __tablename__ = 'expenses'
    __table_args__ = {'schema': 'travel'} 


    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Float, nullable = False)
    description = db.Column(db.String(300))

    trip_id = db.Column(db.Integer, db.ForeignKey('travel.trips.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('travel.categories.id'))

    # Define relationships
    trip_location = db.relationship("Trip", back_populates="expenses")
    category = db.relationship("Category", back_populates="expenses")
                        
class ExpenseSchema(ma.Schema):
    description = String(validate=Length(min=2, error="Description must be at least 2 characters"))

    # Nested fields
    trip_location = fields.Nested('TripSchema', only=['location'])
    category = fields.Nested('CategorySchema', only=['name'])

    class Meta:
        fields = ('id', 'amount', 'description', 'trip_location', 'category')

one_expense = ExpenseSchema()
many_expenses = ExpenseSchema(many = True)
expense_without_id = ExpenseSchema(exclude=['id'])
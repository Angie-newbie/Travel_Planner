from init import db, ma

class Category(db.Model):
    __tablename__ = 'categories'
    __table_args__ = {'schema': 'travel'} 


    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique=True)

                        
class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

one_category = CategorySchema()
many_categories = CategorySchema(many = True)
category_without_id = CategorySchema(exclude=['id'])
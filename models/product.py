from db import db

class ProductModel(db.Model): #a model for storing data about products.
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)  #This id maps to product_id in reviews
    name = db.Column(db.String(80), unique=True, nullable=False)
    overall_satisfaction = db.Column(db.Float, nullable=False)
    reviews = db.relationship("ReviewModel", back_populates="product", lazy="dynamic")
        #a relationship with the ReviewModel class. 
        # The back_populates parameter specifies the name of the relationship in the ReviewModel class that links back to the ProductModel class. 
        # The lazy parameter specifies how the related objects should be loaded from the database.
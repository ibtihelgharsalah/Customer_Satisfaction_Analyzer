from db import db

class ReviewModel(db.Model): #a model for storing data about reviews.
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), unique=False, nullable=False)
    sentiment = db.Column(db.String(80), nullable=False)
    product = db.relationship("ProductModel", back_populates="reviews")
        #a relationship with the ProductModel class. 
        #The back_populates parameter specifies the name of the relationship in the ProductModel class that links back to the ReviewModel class.

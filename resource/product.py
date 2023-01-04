import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import ProductModel
from schemas import ProductSchema
from models import ReviewModel
from schemas import  ReviewSchema, ReviewUpdateSchema
from sqlalchemy.orm import sessionmaker

# defining a Flask blueprint called blp that provides a RESTful API for performing operations on "products".
blp = Blueprint("products", __name__, description="Operations on products")

# defining a method that specifies the overall satisfaction for a product
def get_product_sentiment(sents):
    # Initialize a count of positive and negative reviews
    positive_count = 0
    negative_count = 0
    
    # Iterate over the review sentiments and count the number of positive and negative reviews
    for sent in sents:
        if sent == "positive":
            positive_count += 1
        elif sent == "negative":
            negative_count += 1
    
    # Calculate the overall satisfaction as the percentage of positive reviews
    overall_satisfaction = positive_count / (positive_count + negative_count)
    
    return overall_satisfaction


@blp.route("/product/<string:product_id>")
class Product(MethodView):
    # The "Product" class is a Flask MethodView that provides a GET method for retrieving 
    # a single product by its id. 
    @blp.response(200, ProductSchema) 
    def get(self, product_id): #get a product given a product_id
        # The method uses the "ProductModel" to query the database and returns the product or a 404 error if 
        # the product is not found.
        product = ProductModel.query.get_or_404(product_id)
        return product

@blp.route("/product")
class ProductList(MethodView):
    # The ProductList class is a Flask MethodView that provides a GET method for retrieving a list of 
    # all products and a POST method for creating a new product.
    @blp.response(200, ProductSchema(many=True)) 
    def get(self): #get a list of all products
        # The GET method uses the ProductModel to query the database and returns the list of products.
        return ProductModel.query.all()

    @blp.arguments(ProductSchema)
    @blp.response(200, ProductSchema)  
    def post(self, product_data, review_data): # add a new product to the database
        
        # Create a session to execute queries
        Session = sessionmaker(ReviewModel)
        session = Session()
        
        # Execute a SELECT query to fetch the review sentiment column where product id is specified
        review_sents = session.query(review_data["sentiment"]).all()

        # Create an array to store the review sentiments
        review_sents_array = []

        # Iterate over the review sentiment tuples and add the text to the array
        for review_sent in review_sents:
            review_sents_array.append(review_sent)
                    
        satisfaction = get_product_sentiment(review_sents_array)
        
        # Add the overall satisfaction to the product data
        product_data['overall_satisfaction'] = satisfaction
         
        product = ProductModel(**product_data)
        try:
            db.session.add(product)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A product with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the product.")

        return product #Marshmallow can turn an object or dictionnary into JSON
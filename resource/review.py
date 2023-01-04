import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import ReviewModel
from schemas import  ReviewSchema, ReviewUpdateSchema

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# defining the sentiment analysis model method (VADER)
def predict_sentiment(sentence):
    nltk.download('vader_lexicon')
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(sentence)['compound']
    if (score>0):
        return "Positive"
    elif (score == 0):
        return "Neutral"
    else:
        return "Negative"

# defining a Flask blueprint called blp that provides a RESTful API for performing operations on "reviews".
blp = Blueprint("reviews", __name__, description="Operations on reviews")

@blp.route("/review/<string:review_id>")
class Review(MethodView):

    @blp.response(200, ReviewSchema)
    def get(self, review_id): #get a review given a review_id
        review = ReviewModel.query.get_or_404(review_id)
        return review
        
    def delete (self, review_id): #delete a review given a review_id
        review = ReviewModel.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()
        return {"message": "review deleted."}
    

    @blp.arguments(ReviewUpdateSchema)
    @blp.response(200, ReviewSchema)
    def put (self, review_data, review_id): #update a review body given a review_id
        review = ReviewModel.query.get_or_404(review_id)

        if review:
            review.price = review_data["body"]
        else:
            review = ReviewModel(**review_data)
            
        db.session.add(review)
        db.session.commit()

        return review


@blp.route("/review")
class ReviewList(MethodView):

    @blp.response(200, ReviewSchema(many=True))
    def get(self): #get a list of all reviews
        return ReviewModel.query.all()

    @blp.arguments(ReviewSchema)
    @blp.response(201, ReviewSchema)
    def post(self, review_data): #add a new review to the database
        
        # Use the sentiment analysis model to predict the sentiment of the review text
        sentiment = predict_sentiment(review_data['body'])
        
        # Add the sentiment prediction to the review data
        review_data['sentiment'] = sentiment
        review = ReviewModel(**review_data)  

        try:
            db.session.add(review)
            db.session.commit()  
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the review.")

        return review
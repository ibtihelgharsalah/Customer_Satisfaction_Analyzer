# Customer Satisfaction Analyzer

a RESTful API that allows businesses to measure the
satisfaction of their customers in real-time.

## Database

uses a database composed of two tables : "Products" and "Reviews".
The relationship between the ”products” and ”reviews” tables is a one-to-many relationship, as a single product can have multiple reviews, but each review is associated with only one product.

## NLP - Sentiment analysis

uses the NLP pre-trained model, VADER, to conduct sentiment analysis on reviews of specific products.

## User-defined method - Product Satisfaction

uses a python method to calculate the overall satisfaction of a specified product and returns the proportion of positive reviews among all reviews.

## HTTP Requests
performs 2 GETters and 1 POSTer on the "Products" table and 2 GETters, 1 POSTer, 1 DELETEr and 1 PUTter on the "Reviews" table.

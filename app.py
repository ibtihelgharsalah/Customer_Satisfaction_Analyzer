import os

from flask import Flask
from flask_smorest import Api

from db import db    
import models

from resource.review import blp as ReviewBlueprint
from resource.product import blp as ProductBlueprint

#We put all instructions inside a function
def create_app(db_url=None):
    #when calling this function, we can pass in a database URL that we want to connect to
    #Creating a Flask app
    app = Flask(__name__, instance_path=os.getcwd())
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Customer Statisfaction API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
            "OPENAPI_SWAGGER_UI_URL"
        ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    #Initializeing the Flask-SQLAlchemy extension
    db.init_app(app)
    
    #Creating an API object using Api(app) from the Flask-Smorest library 
    api = Api(app)

    #Defining a "before_first_request" handler that creates the database tables when the app starts.
    @app.before_first_request
    def create_tables():
        db.create_all()

    #Registering two blueprints with the API: "ReviewBlueprint" and "ProductBlueprint"
    api.register_blueprint(ReviewBlueprint)
    api.register_blueprint(ProductBlueprint)
    return app
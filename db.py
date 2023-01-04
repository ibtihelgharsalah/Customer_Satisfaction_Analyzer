from flask_sqlalchemy import SQLAlchemy

#creating a new instance of the SQLAlchemy class called "db".
db = SQLAlchemy()

#The db instance is now the entry point for interacting with the database using SQLAlchemy. 
#We can use it to define the schema of our database, create and drop tables, query the database, and more.
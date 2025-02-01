from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os


app = Flask(__name__)
# wrap app in cors to allow cross origin requests
CORS(app)

# location of database in machine
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

# Not track all modifications to database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

# Create an engine and bind the sessionmaker to it
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"]) 
Session = sessionmaker(bind=engine) 
session = Session()
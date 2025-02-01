# Create, Read, Update, Delete (CRUD) operations for the API
from flask import Blueprint, current_app, request, jsonify, send_from_directory
from config import app, db
from models import User
import os


@app.route('/', methods=["GET"])
def home():
    return jsonify({"message": "WORK!!!"}),200


# if run file then execute the code in this file only
if __name__ == '__main__':
    # when start, create db if not already have db
    # cretae all the tables in the database
    with app.app_context():
        db.create_all()
    # run the app
    app.run(debug=True)
# Create, Read, Update, Delete (CRUD) operations for the API
from flask import Blueprint, current_app, request, jsonify, send_from_directory
from config import app, db
from models import User, UserSkill, Skill
import requests
import utils
from dotenv import load_dotenv
import os
import csv


# Load environment variables from the .env file
load_dotenv()

@app.route('/', methods=["GET"])
def home():
    users = User.query.all()  # Get all users from the database
    users_json = [user.to_json() for user in users]  # Convert each user to JSON

    return jsonify(users_json)  # Return as JSON


# @app.route('/', methods=["POST"])
# def UserData():

#     api_key = ''
#     headers = {'Authorization': 'Bearer ' + api_key}
#     api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
#     linkedin_profile_url = 'https://www.linkedin.com/in/williamhgates'

#     response = requests.get(api_endpoint,
#                         params={'url': linkedin_profile_url, 
#                                 },
#                         headers=headers)
#     result = response.json()
#     return result



# @app.route('/linkedinProfile', methods=["POST"])
# def UserData():
#     # get user url from frontend
    



#     # call proxycurl api to get user data into categories
    
#     headers = {'Authorization': 'Bearer ' + os.getenv("api_key")}
#     api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
#     linkedin_profile_url = 'https://www.linkedin.com/in/williamhgates'

#     response = requests.get(api_endpoint,
#                         params={'url': linkedin_profile_url, 
#                                 },
#                         headers=headers)
#     student = response.json()



#     # mentor data that match with user skills?


#     # call AI API for analysis

    




#     return jsonify({"message": "WORK!!!"})


# @app.route('/', methods=["POST"])
# def loaddb():
#     utils.load_csv_to_db("mock_profiles.csv")

#     return jsonify({"message": "OKEU"}),200



# if run file then execute the code in this file only
if __name__ == '__main__':
    # when start, create db if not already have db
    # cretae all the tables in the database
    with app.app_context():
        db.create_all()
    # run the app
    app.run(debug=True)
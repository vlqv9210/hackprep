# Create, Read, Update, Delete (CRUD) operations for the API
from flask import Blueprint, current_app, request, jsonify, send_from_directory
from config import app, db
from models import User, UserSkill, Skill
import requests
import utils
from datetime import date
from dotenv import load_dotenv
import os
import csv



# Load environment variables from the .env file
load_dotenv()

from flask import jsonify

@app.route('/', methods=["GET"])
def home():
    users = User.query.all()  # Get all users from the database
    return jsonify([user.to_json() for user in users])  # ✅ Convert to JSON



# @app.route('/', methods=["POST"])
# def UserData():
#     api_key = '5OowENhf0gUjDqxmLGf9YA'
#     headers = {'Authorization': 'Bearer ' + api_key}
#     api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
#     linkedin_profile_url = 'https://www.linkedin.com/in/beatrizda/'

#     response = requests.get(api_endpoint,
#                         params={'url': linkedin_profile_url, 'skills': 'include'
#                                 },
#                         headers=headers)
#     result = response.json()
#     return result



@app.route('/linkedinProfile', methods=["POST"])
def UserData():
    # get client url from frontend
    client_url = request.json.get("linkedin_url")


    # call proxycurl api to get user data into categories
    api_key = os.getenv("API_KEY")
    headers = {'Authorization': 'Bearer ' + api_key}
    api_endpoint = os.getenv("API_ENDPOINT")

    response = requests.get(api_endpoint,
                        params={'url': client_url, 
                                'skills': 'include'},
                        headers=headers)
    client = response.json()

    # calculate client years of experience
    client_experience = client["experiences"]

    client_year_experience = 0
    for company in client_experience:
        start_day = company["starts_at"]
        # ends_at = company["ends_at"] != None ? company["ends_at"] : date.today()
        





    # get client skill




    # mentor data that match with user skills?
    # get mentor that match at least 2 skills with client
    # mentor experiences must be larger than client




    # call AI API for analysis
    # put mentor with client in to get top 10
    # generate the prompt




    # return the result to frontend as json object

    




    return jsonify({"message": "WORK!!!"})


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
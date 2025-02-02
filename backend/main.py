# Create, Read, Update, Delete (CRUD) operations for the API
from flask import Blueprint, current_app, request, jsonify, send_from_directory
from config import app, db
# from models import User
import requests

from dotenv import load_dotenv
import os
import csv


# Load environment variables from the .env file
load_dotenv()

@app.route('/', methods=["GET"])
def home():
    return jsonify({"message": "WORK!!!"}),200

# @app.route('/', methods=["POST"])
# def UserData():

#     api_key = '5OowENhf0gUjDqxmLGf9YA'
#     headers = {'Authorization': 'Bearer ' + api_key}
#     api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
#     linkedin_profile_url = 'https://www.linkedin.com/in/williamhgates'

#     response = requests.get(api_endpoint,
#                         params={'url': linkedin_profile_url, 
#                                 },
#                         headers=headers)
#     result = response.json()
#     return result



@app.route('/linkedinProfile', methods=["POST"])
def UserData():
    # get user url from frontend
    linkedin_profile_url = request.json.get("linkedin_profile_url")


    # call proxycurl api to get user data into categories
    api_key = os.getenv('API_KEY')
    headers = {'Authorization': 'Bearer ' + api_key}
    api_endpoint = os.getenv('API_ENDPOINT')
    params = {
        'url': linkedin_profile_url
    }

    response = requests.get(api_endpoint, params=params, headers=headers)
    
    result = response.json()



    # mentor data that match with user skills?







    # call AI API for analysis
    csv_file = 'mock_profiles.csv'
    json_data = csv_to_json(csv_file)

    




    return jsonify({"message": "WORK!!!"})



# if run file then execute the code in this file only
if __name__ == '__main__':
    # when start, create db if not already have db
    # cretae all the tables in the database
    with app.app_context():
        db.create_all()
    # run the app
    app.run(debug=True)
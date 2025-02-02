# Create, Read, Update, Delete (CRUD) operations for the API
from flask import Blueprint, current_app, request, jsonify, send_from_directory
from config import app, db
from models import User, UserSkill, Skill
import requests
import json
import utils
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
#     api_key = ''
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
    # client_url = request.json.get("linkedin_url")
    client_url = "https://www.linkedin.com/in/vy-vuong-b29a17287/"


    # call proxycurl api to get user data into categories
    api_key = os.getenv("API_KEY")
    headers = {'Authorization': 'Bearer ' + api_key}
    api_endpoint = os.getenv("API_ENDPOINT")

    response = requests.get(api_endpoint,
                        params={'url': client_url, 
                                'skills': 'include'},
                        headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch LinkedIn data"}), 500
    

    client = response.json()

    # calculate client years of experience
    client_experience = client["experiences"]
    client_year_experience = utils.calculate_total_experience(client_experience)

    # get client skill
    client_skills = client["skills"]



    # mentor data that match with user skills?
    # get mentor that match at least 2 skills with client
    # mentor experiences must be larger than client
    mentor = utils.find_matching_mentors(client_skills=client_skills, client_year_experience=client_year_experience)



    # call AI API for analysis
    # put mentor with client in to get top 10
    # generate the prompt
    prompt = f'''
         Evaluate the compatibility between this student and mentor based on skills, and experience.

        Student:
        {client}

        Mentor list:
        {mentor}

        Provide a match score from 0 to 100 and a short explanation. And also the template to message them.
        Give us the top ten mentor for this client in a json format look like this

        'name': mentor name,
        'job_title': mentor job title,
        'skills': mentor skill,
        'education': mentor education,
        'experience': mentor experience,
        'score' : score,
        'explanation' : reason,
        'cold_message' : message

    '''


    mentor_response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('AI_API_KEY')}",

        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1:free", 
            "messages": [
            {
                "role": "user",
                "content": prompt  
            }
            ]
        })
    )

    if mentor_response.status_code != 200:
        return jsonify({"error": "Failed to fetch AI analysis"}), 500


    mentor_data = mentor_response.json()  # Extract JSON response

    # mentor_content = mentor_data["content"]

    return jsonify({"message": mentor_data}), 200  # ✅ Corrected


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
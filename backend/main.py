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


@app.route('/linkedinProfile', methods=["POST"])
def UserData():
    # get client url from frontend
    # client_url = request.json.get("linkedin_url")
    client_url = os.getenv('client_url')


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

        Provide a match score from 0 to 100 and a short explanation. And also the template to message the mentor.
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
        url= os.getenv('AI_API'),
        headers={
            "Authorization": f"Bearer {os.getenv('AI_API_KEY')}",
        },
        data=json.dumps({
            "model": "meta-llama/llama-3.2-3b-instruct:free", # Optional
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
    
    # Use .json() method to extract response as a dictionary
    mentor_data = mentor_response.json()

    # Step 1: Isolate the JSON string from the content
    json_part = mentor_data["content"].split('`json\n')[1].split('`')[0]

    # Step 2: Parse the JSON string into a Python list of dictionaries
    mentors = json.loads(json_part)

    # Step 3: Create the desired output
    formatted_mentor_list = []

    for mentor in mentors:
        formatted_mentor = {
            'name': mentor['name'],
            'job_title': mentor['job_title'],
            'skills': mentor['skills'],
            'education': mentor['education'],
            'experience': mentor['experience'],
            'score': mentor['score'],
            'explanation': mentor['explanation'],
            'cold_message': mentor['cold_message']
        }
        formatted_mentor_list.append(formatted_mentor)

    return jsonify({"message": formatted_mentor_list}), 200  



# test manually
@app.route('/testAIApi', methods=["POST"])
def testAPI():

    prompt = f'''
        Evaluate the compatibility between this student and mentor based on skills, and experience.

        Student:
        name: Vy
        skill: data analysis
        year experiences: 2

        Mentor list:
        William French,Machine Learning Engineer,"Austin, TX",B.A. in Computer Science,34,"Srum, AWS, Docker, Program management, Data Analysis",http://reeves-conley.com/
        Kimberly White,Software Engineer,"Sydney, Australia",B.S. in Computer Science,27,"SQL, React, Node.js, Data Analysis, Agile",http://perez.com/
        Brianna Macias,Full Stack Developer,"London, UK",B.A. in Computer Science,37,"AWS, Machine Learning, React, Software Design, C#",https://becker-perkins.info/
        John Baker,DevOps Engineer,"Los Angeles, CA",M.S. in Computer Science,31,"Problem Solving, AWS, Python, Software Architecture, CSS",http://andrews.com/
        Christopher Cooper,Frontend Developer,"London, UK",B.S. in Computer Science,30,"Deep Learning, Machine Learning, Srum, Node.js, Kubernetes",http://sullivan-holmes.org/
        Ashley Zuniga DVM,DevOps Engineer,"Seoul, South Korea",B.A. in Information Technology,16,"Program management, Srum, Java, Team Leadership, Cloud Computing",https://nelson.com/
        Robin Davila,AI Specialist,"Sydney, Australia",M.S. in Data Science,12,"Problem Solving, Cloud Computing, Team Leadership, Python, SQL",http://olson.com/
        Diane Murray,DevOps Engineer,"Paris, France",M.S. in Data Science,31,"Cloud Computing, Communication, HTML, User Interface DesignSoftware Development, Deep Learning",https://caldwell.com/
        Kevin Hawkins,Software Engineer,"San Diego, CA",B.S. in Computer Science,17,"Srum, Node.js, HTML, Python, Problem Solving",http://www.taylor.com/
        Nicole Gibson,Data Scientist,"London, UK",B.S. in Computer Engineering,40,"Machine Learning, Docker, Software Architecture, Communication, Team Leadership",http://www.english.net/
        Leonard Johnson,DevOps Engineer,"San Francisco, CA",B.S. in Computer Engineering,13,"Python, PyTorch, Java, C#, Communication",https://reyes.com/
        Jessica Gomez,Software Engineer,"San Diego, CA",B.A. in Computer Science,37,"User Interface DesignSoftware Development, Docker, Agile, TensorFlow, C#",http://evans.com/
        Julie Ashley,Software Engineer,"Chicago, IL",B.S. in Computer Science,39,"Docker, Python, C++, Deep Learning, C#",https://www.gray.com/
        Mary Perry,Backend Developer,"New York, NY",M.S. in Computer Engineering,35,"C#, Agile, Problem Solving, Team Leadership, Software Architecture",https://www.miller-sosa.org/
        Jasmine Snyder,DevOps Engineer,"Sydney, Australia",B.S. in Computer Science,29,"Software Design, HTML, Communication, Deep Learning, React",http://stewart.net/
        Daniel Gonzalez,AI Specialist,"London, UK",B.A. in Computer Science,7,"Software Architecture, Java, SQL, Data Analysis, CSS",https://chambers.com/
        Christopher Leon,Software Engineer,"New York, NY",B.S. in Computer Engineering,9,"Project Management, HTML, Communication, Deep Learning, AWS",https://lee-reynolds.info/
        Brandon Carlson,AI Specialist,"Berlin, Germany",B.S. in Computer Engineering,17,"Program management, PyTorch, Problem Solving, HTML, Kubernetes",http://miller.net/
        Logan Camacho,Full Stack Developer,"San Diego, CA",M.S. in Data Science,39,"Machine Learning, Software Architecture, User Interface DesignSoftware Development, Communication, Program management",http://stephenson.com/
        Anthony Berger,Machine Learning Engineer,"Austin, TX",B.A. in Information Technology,38,"PyTorch, Communication, Machine Learning, Node.js, Srum",http://www.raymond.com/
        Dr. Amanda Jones,Frontend Developer,"Toronto, Canada",B.A. in Information Technology,18,"Docker, PyTorch, Program management, Machine Learning, Project Management",https://clark.com/
        Lisa Walker,Software Engineer,"Seoul, South Korea",M.S. in Data Science,21,"Deep Learning, User Interface DesignSoftware Development, Python, Software Design, AWS",http://www.thompson.com/
        George Booker,UX Designer,"New York, NY",B.A. in Information Technology,33,"TensorFlow, C++, User Interface DesignSoftware Development, Machine Learning, PyTorch",http://www.villa.com/
        

        Provide a match score from 0 to 100 and a short explanation. And also the template to message them.
        Give us the top ten mentor for each client in a json format look like this

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
        url=os.getenv('AI_API'),
        headers={
            "Authorization": f"Bearer {os.getenv('AI_API_KEY')}",
        },
        data=json.dumps({
            "model": "meta-llama/llama-3.2-3b-instruct:free", # Optional
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

    # Use .json() method to extract response as a dictionary
    mentor_data = mentor_response.json()

    # Check if 'choices' exists and contains at least one item
    if 'choices' not in mentor_data or len(mentor_data['choices']) == 0:
        return jsonify({"error": "'choices' key is missing or empty in the response"}), 500

    # Extract the 'content' key from the first choice in the response
    content = mentor_data['choices'][0]['message']['content']

    # Print the content for debugging
    print("Content:", content)

    # Step 1: Isolate the JSON string from the content
    json_part = content.split('```json\n')[1].split('```')[0]

    # Step 2: Parse the JSON string into a Python list of dictionaries
    mentors = json.loads(json_part)

    # Step 3: Create the desired output
    formatted_mentor_list = []

    for mentor in mentors:
        formatted_mentor = {
            'name': mentor['name'],
            'job_title': mentor['job_title'],
            'skills': mentor['skills'],
            'education': mentor['education'],
            'experience': mentor['experience'],
            'score': mentor['score'],
            'explanation': mentor['explanation'],
            'cold_message': mentor['cold_message']
        }
        formatted_mentor_list.append(formatted_mentor)

    return jsonify({"message": formatted_mentor_list}), 200



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
# Create, Read, Update, Delete (CRUD) operations for the API
from flask import Blueprint, current_app, request, jsonify, send_from_directory
from config import app, db
from models import User, UserSkill, Skill
import requests
import json
import utils
from dotenv import load_dotenv
import os
from groq import Groq


# Load environment variables from the .env file
load_dotenv()

from flask import jsonify

@app.route('/', methods=["GET"])
def home():
    users = User.query.all()  # Get all users from the database
    return jsonify([user.to_json() for user in users])  


@app.route('/testGetData', methods=["POST"])
def testGetData():
    client_url = request.json.get("linkedin_url")

    return jsonify({"message" : client_url}), 200



# I comment this out to prevent 
@app.route('/linkedinProfile', methods=["POST"])
def UserData():
    # get client url from frontend
    client_url = request.json.get("linkedin_url")
    # client_url = os.getenv('client_url')


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
        Samantha Hernandez,UX Designer,"San Francisco, CA",M.S. in Data Science,38,"Cloud Computing, Deep Learning, Software Design, Communication, Project Management",http://www.anderson.com/
        Marcus James,AI Specialist,"Sydney, Australia",B.S. in Computer Engineering,34,"HTML, Data Analysis, Program management, Cloud Computing, Team Leadership",https://www.meyers-lewis.com/
        Christina Hurst,UX Designer,"Berlin, Germany",B.A. in Computer Science,38,"C++, HTML, Software Architecture, Deep Learning, Project Management",http://www.kennedy.com/
        Kayla Coleman,UX Designer,"San Diego, CA",M.S. in Computer Science,30,"Node.js, Project Management, Java, Team Leadership, Python",http://johnston.info/
        Brandon Bautista,Software Engineer,"San Diego, CA",B.S. in Computer Science,15,"Deep Learning, Software Design, C, TensorFlow, PyTorch",http://smith-griffin.com/
        Amanda Black,Full Stack Developer,"Toronto, Canada",B.S. in Computer Science,27,"User Interface DesignSoftware Development, TensorFlow, Python, Cloud Computing, Srum",https://hickman.com/
        Brittany Bautista,DevOps Engineer,"Paris, France",B.A. in Information Technology,29,"Program management, Deep Learning, Machine Learning, C#, HTML",https://www.reyes-weaver.org/
        Ronald Foster,Machine Learning Engineer,"Los Angeles, CA",Ph.D. in Artificial Intelligence,23,"Srum, Data Analysis, React, Kubernetes, Project Management",https://www.tate.com/
        Jennifer Garcia,Full Stack Developer,Singapore,M.S. in Computer Engineering,34,"HTML, Software Architecture, Deep Learning, Kubernetes, Team Leadership",http://www.cain-riley.org/
        Amber Carroll,Data Scientist,"Seattle, WA",B.S. in Computer Science,30,"Program management, Kubernetes, Project Management, Data Analysis, Docker",https://griffith.com/
        Tonya Miller,Software Engineer,"Sydney, Australia",B.S. in Computer Engineering,26,"Cloud Computing, Agile, User Interface DesignSoftware Development, Python, Docker",http://www.santiago.org/
        Emily Weeks,Machine Learning Engineer,"Atlanta, GA",B.A. in Information Technology,21,"Software Design, C#, SQL, Team Leadership, Problem Solving",http://www.smith.com/
        Nancy Morris,Frontend Developer,"Los Angeles, CA",B.S. in Electrical Engineering,28,"Team Leadership, User Interface DesignSoftware Development, Java, Kubernetes, Program management",https://www.allen.org/
        Kendra King,Frontend Developer,"Seoul, South Korea",B.A. in Information Technology,36,"Node.js, Data Analysis, Kubernetes, User Interface DesignSoftware Development, C#",https://www.harmon.info/
        Nicole Myers,Frontend Developer,"New York, NY",B.S. in Electrical Engineering,27,"Problem Solving, C++, Team Leadership, Node.js, Docker",https://www.mendez.net/
        Amanda Mccarthy PhD,Machine Learning Engineer,"Toronto, Canada",M.S. in Computer Science,31,"Deep Learning, Machine Learning, Python, Srum, React",http://shepherd.com/
        Kristen Watson,Frontend Developer,"San Diego, CA",B.S. in Computer Engineering,15,"Program management, Python, Software Architecture, Java, TensorFlow",https://castillo-lam.info/
        Michael Clark,AI Specialist,"Seattle, WA",M.S. in Data Science,23,"Java, Kubernetes, Srum, Cloud Computing, User Interface DesignSoftware Development",https://morrison-harrell.com/
        Christina Anderson,Data Scientist,"San Diego, CA",M.S. in Computer Engineering,14,"User Interface DesignSoftware Development, PyTorch, Data Analysis, Deep Learning, Software Design",https://www.rasmussen.biz/
        Lauren Stephens,AI Specialist,"Seoul, South Korea",B.A. in Information Technology,32,"CSS, Docker, Agile, Machine Learning, C#",http://www.williams-haynes.com/
        Charles Wilson,Backend Developer,"Los Angeles, CA",B.A. in Computer Science,39,"CSS, HTML, Node.js, AWS, Python",http://jenkins.com/
        Olivia Martinez,Software Engineer,"Seoul, South Korea",M.S. in Data Science,29,"Java, Software Architecture, Docker, CSS, Data Analysis",https://www.smith-robinson.com/
        Amy Herrera,Full Stack Developer,"London, UK",M.S. in Computer Engineering,33,"Data Analysis, HTML, CSS, Agile, Communication",https://roy.biz/
        Linda Martinez,Backend Developer,"Paris, France",B.S. in Electrical Engineering,17,"Srum, TensorFlow, SQL, Software Architecture, Program management",http://stevenson-martin.com/
        Joshua Allen,DevOps Engineer,"San Diego, CA",B.S. in Computer Engineering,7,"Team Leadership, SQL, C#, Project Management, User Interface DesignSoftware Development",https://flores.com/
        Gabriel Robinson,Full Stack Developer,"Berlin, Germany",M.S. in Computer Engineering,37,"Cloud Computing, AWS, PyTorch, Software Design, SQL",https://benjamin.com/
        Alexandria Bray,Product Manager,"Chicago, IL",M.S. in Data Science,5,"Cloud Computing, Kubernetes, Deep Learning, SQL, C",http://www.stein-sandoval.com/
        Michael Little,Machine Learning Engineer,Singapore,M.S. in Data Science,16,"C++, Software Architecture, Deep Learning, Machine Learning, Program management",https://www.simpson.com/
        Charles Chan,Software Engineer,"Austin, TX",M.S. in Computer Science,6,"C, User Interface DesignSoftware Development, HTML, Software Architecture, Deep Learning",http://www.carpenter.com/
        Terry Jones,Backend Developer,"Seoul, South Korea",M.S. in Computer Engineering,35,"Deep Learning, Software Design, TensorFlow, Machine Learning, Project Management",http://www.cruz.biz/
        Mary Barnes,Product Manager,"San Francisco, CA",B.A. in Information Technology,8,"Software Architecture, Agile, AWS, Data Analysis, SQL",https://santiago.biz/
        Timothy Russell,Backend Developer,"Atlanta, GA",B.S. in Computer Science,32,"Docker, SQL, Java, Node.js, Software Design",https://smith-williams.biz/
        Jonathan Hurst,Backend Developer,"Seoul, South Korea",B.S. in Computer Science,22,"Team Leadership, TensorFlow, Deep Learning, Node.js, Data Analysis",http://www.gonzalez.info/
        Daniel Ford,Full Stack Developer,"Paris, France",B.A. in Computer Science,27,"C++, Docker, CSS, C#, TensorFlow",http://www.burton.net/
        Kristina Freeman,Data Scientist,"London, UK",B.A. in Information Technology,18,"Node.js, Java, Problem Solving, Python, C#",https://berry-kaiser.net/
        Benjamin Kidd,Software Engineer,"London, UK",Ph.D. in Artificial Intelligence,9,"Srum, CSS, Communication, HTML, C++",http://fisher.com/
        Stephanie Howell,Software Engineer,"Sydney, Australia",M.S. in Computer Science,19,"Deep Learning, TensorFlow, Project Management, C++, Machine Learning",http://miller.com/
        Steven Rivera,Software Engineer,"Toronto, Canada",B.S. in Electrical Engineering,10,"Python, Project Management, Docker, AWS, HTML",http://www.joyce.net/
        Ashley Rush,AI Specialist,"London, UK",B.S. in Electrical Engineering,22,"Agile, C++, Node.js, Data Analysis, Docker",http://www.weeks.org/
        Kenneth Wood,Data Scientist,"San Diego, CA",Ph.D. in Artificial Intelligence,9,"React, C++, Deep Learning, Program management, AWS",https://robinson.com/
        Albert Russell,UX Designer,"Chicago, IL",M.S. in Computer Science,18,"Team Leadership, C#, PyTorch, Machine Learning, CSS",https://west-cook.com/
        Thomas Ewing,Data Scientist,"Berlin, Germany",B.S. in Electrical Engineering,7,"User Interface DesignSoftware Development, TensorFlow, Kubernetes, C, Python",https://www.harrison.com/
        Steven Bailey,Machine Learning Engineer,"Seattle, WA",B.S. in Electrical Engineering,31,"HTML, Cloud Computing, Software Design, C, Program management",https://strong.com/
        Debbie Kane,AI Specialist,"Sydney, Australia",M.S. in Computer Engineering,17,"C++, Data Analysis, TensorFlow, Java, C",https://www.gray-rowland.net/
        Kelsey Ferguson,Product Manager,"Seattle, WA",M.S. in Computer Engineering,14,"Python, SQL, Docker, User Interface DesignSoftware Development, Java",https://hernandez.com/
        Samantha Collins,Software Engineer,"Sydney, Australia",M.S. in Data Science,39,"Kubernetes, Team Leadership, CSS, C#, C++",http://guzman.com/
        Summer Bailey,Product Manager,"Sydney, Australia",Ph.D. in Artificial Intelligence,16,"Kubernetes, Problem Solving, AWS, C++, Agile",https://www.day.com/
        Devin Smith,UX Designer,"San Diego, CA",B.S. in Computer Science,32,"C, Kubernetes, Machine Learning, AWS, Project Management",https://hill-zamora.org/
        Heather Silva,UX Designer,"Los Angeles, CA",M.S. in Data Science,14,"Deep Learning, Docker, React, C, Communication",https://blake.com/
        Johnathan Williams,DevOps Engineer,"Chicago, IL",M.S. in Data Science,7,"PyTorch, Data Analysis, CSS, Team Leadership, Kubernetes",https://www.hoffman-miller.com/
        Erik Hamilton,UX Designer,"Austin, TX",M.S. in Computer Engineering,8,"Kubernetes, Agile, HTML, Docker, Problem Solving",https://smith-cruz.org/
        Jessica Brewer,DevOps Engineer,"Chicago, IL",B.S. in Electrical Engineering,34,"Cloud Computing, C#, Software Design, C++, Docker",https://hogan.com/
        
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
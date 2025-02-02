import csv
from flask import Flask, request
from sqlalchemy.orm import sessionmaker
from config import db
from models import User, UserSkill, Skill  # Import models

app = Flask(__name__)

# Function to load CSV data and insert into the database
def load_csv_to_db(csv_file_path):
    with open(csv_file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header row if there's one
        
        session = sessionmaker(bind=db.engine)()  # Create a session
        for row in csvreader:
            # Unpack the CSV data
            name, jobTitle, location, education, years_of_experience, skills_str, linkedin_profile = row
            
            # Process years_of_experience and handle missing values
            try:
                years_of_experience = int(years_of_experience) if years_of_experience else None
            except ValueError:
                years_of_experience = None

            skills = skills_str.split(',')  # Assuming skills are comma-separated in the CSV
            
            # Check if user already exists
            user = session.query(User).filter_by(name=name).first()
            if not user:
                user = User(
                    name=name,
                    jobTitle=jobTitle,
                    city=location,
                    education=education,
                    years_of_experience=years_of_experience,
                    linkedin_profile=linkedin_profile
                )
                session.add(user)
                session.commit()

            # Add skills to user
            for skill_name in skills:
                skill = session.query(Skill).filter_by(name=skill_name.strip()).first()
                if not skill:
                    skill = Skill(name=skill_name.strip())
                    session.add(skill)
                    session.commit()
                
                # Add user-skill relation
                user_skill = UserSkill(user_id=user.id, skill_id=skill.id)
                session.add(user_skill)

        session.commit()


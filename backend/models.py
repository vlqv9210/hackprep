from flask import request
from sqlalchemy.orm import sessionmaker
from config import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    jobTitle = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    education = db.Column(db.String(80), nullable=False)
    years_of_experience = db.Column(db.Integer, nullable=True)
    linkedin_profile = db.Column(db.String(200), nullable=True)
    skills = db.relationship('UserSkill', backref='user', lazy=True)

    def __init__(self, name, jobTitle, city, education, years_of_experience, linkedin_profile):
        self.name = name
        self.jobTitle = jobTitle
        self.city = city
        self.education = education
        self.years_of_experience = years_of_experience
        self.linkedin_profile = linkedin_profile

    def to_json(self):
        return {
            "name": self.name,
            "jobTitle": self.jobTitle,
            "city": self.city,
            "education": self.education,
            "years_of_experience": self.years_of_experience,
            "linkedin_profile": self.linkedin_profile,
            "skills": [skill.to_json() for skill in self.skills]
        }

class Skill(db.Model):
    __tablename__ = 'skill'
    name = db.Column(db.String(80), primary_key=True, unique=True)

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {
            "name": self.name,
        }

class UserSkill(db.Model):
    __tablename__ = 'user_skill'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill_name = db.Column(db.String(80), db.ForeignKey('skill.name'), nullable=False)

    def __init__(self, user_id, skill_name):
        self.user_id = user_id
        self.skill_name = skill_name

    def to_json(self):
        return {
            "skill": self.skill_name
        }


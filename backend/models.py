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

    def __init__(self, id, name, jobTitle, city, education, years_of_experience, linkedin_profile):
        self.id = id
        self.name = name
        self.jobTitle = jobTitle
        self.city = city
        self.education = education
        self.years_of_experience = years_of_experience
        self.linkedin_profile = linkedin_profile

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "jobTitle": self.jobTitle,
            "city": self.city,
            "education": self.education,
            "years_of_experience": self.years_of_experience,
            "linkedin_profile": self.linkedin_profile,
        }

class Skill(db.Model):
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class UserSkill(db.Model):
    __tablename__ = 'user_skill'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)

    def __init__(self, user_id, skill_id):
        self.user_id = user_id
        self.skill_id = skill_id

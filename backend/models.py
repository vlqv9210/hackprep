from flask import request
from sqlalchemy.orm import sessionmaker
from config import db

class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(80), primary_key=True, nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=True)
    skill = db.Column(db.String(80), nullable=False)
    areaWork = db.Column(db.String(80), nullable=False)

    def __init__(self, username, skill, areaWork, age=None):
        self.username = username
        self.age = age
        self.skill = skill
        self.areaWork = areaWork

    def to_json(self):
        return {
            "username": self.username,
            "age": self.age,
            "skill": self.skill,
            "areaWork" : self.areaWork

        }
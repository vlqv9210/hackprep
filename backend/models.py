# from flask import request
# from sqlalchemy.orm import sessionmaker
# from config import db

# # deepseek api key
# # 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

# class User(db.Model):
#     __tablename__ = 'user'
#     username = db.Column(db.String(80), primary_key=True, nullable=False, unique=True)
#     jobTitle = db.Column(db.String(80), nullable=False, unique=True)
#     city = db.Column(db.String(80), nullable=False, unique=True)
#     education = db.Column(db.String(80), nullable=False, unique=True)
#     skills = db.relationship('UserSkill', backref='user', lazy=True)


#     def __init__(self, username, jobTitle, city, education, skills):
#         self.username = username
#         self.jobTitle = jobTitle
#         self.city = city
#         self.education = education
#         self.skills = skills

#     def to_json(self):
#         return {
            

#         }


# class UserSkill(db.Model):
#     __tablename__ = 'skill'
#     id = db.Column(db.Integer, primary_key=True)
#     # ondelete='CASCADE' means that if a Pokemon/Skill is deleted, 
#     # this instance will also be deleted.
#     # user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)


# class Skill(db.Model):
#     __tablename__ = 'skill'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)

#     def __init__(self, id, name):
#         self.id = id
#         self.name = name

#     def to_json(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#         }

    



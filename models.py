from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    vacancies = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    skills_required = db.Column(db.String(200), nullable=False)
    experience_required = db.Column(db.String(100), nullable=False)
    ctc = db.Column(db.String(100), nullable=False)


    
class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('resumes', lazy=True))


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    work_experience = db.Column(db.Integer, nullable=False)
    skills = db.Column(db.String(200), nullable=False)
    missing_skills = db.Column(db.String(200), nullable=False)
    post_applied_for = db.Column(db.String(100), nullable=False)
    resume_filename = db.Column(db.String(100), nullable=False)


    
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


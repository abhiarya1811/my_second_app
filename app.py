from models.models import User, Job, Resume, Candidate
from flask import Flask, render_template, request, redirect, url_for, flash , session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
#import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume_matching.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

nltk.download('punkt')
nltk.download('stopwords')


# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle user registration
        username = request.form['username']
        password = request.form['password']
        # Add other user details
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully!', 'success')
        return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle user login
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # Login successful
            session['user_role'] = 'admin' if user.is_admin else 'user'
            # Redirect to user dashboard or admin dashboard based on user role
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')


@app.route('/user_dashboard')
def user_dashboard():
    # Display user dashboard
    return render_template('user_dashboard.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    # Retrieve all candidates from the database
    candidates = Candidate.query.all()
    return render_template('admin_dashboard.html', candidates=candidates)

@app.route('/post_job', methods=['POST'])
def post_job():
    if request.method == 'POST':
        # Retrieve job details from form
        title = request.form['title']
        vacancies = request.form['vacancies']
        location = request.form['location']
        skills_required = request.form['skills_required']
        experience_required = request.form['experience_required']
        ctc = request.form['ctc']
        # Create new job instance
        new_job = Job(title=title, vacancies=vacancies, location=location,
                      skills_required=skills_required, experience_required=experience_required,
                      ctc=ctc)
        # Add new job to the database
        db.session.add(new_job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/update_job/<int:job_id>', methods=['POST'])
def update_job(job_id):
    if request.method == 'POST':
        # Retrieve job details from form
        job = Job.query.get_or_404(job_id)
        job.title = request.form['title']
        job.vacancies = request.form['vacancies']
        job.location = request.form['location']
        job.skills_required = request.form['skills_required']
        job.experience_required = request.form['experience_required']
        job.ctc = request.form['ctc']
        # Update job in the database
        db.session.commit()
        flash('Job updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    if request.method == 'POST':
        # Retrieve job by ID and delete from the database
        job = Job.query.get_or_404(job_id)
        db.session.delete(job)
        db.session.commit()
        flash('Job deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/view_resume/<int:candidate_id>')
def view_resume(candidate_id):
    # Retrieve candidate details by ID
    candidate = Candidate.query.get_or_404(candidate_id)
    # Render template to display resume details
    return render_template('view_resume.html', candidate=candidate)

@app.route('/delete_candidate/<int:candidate_id>', methods=['POST'])
def delete_candidate(candidate_id):
    # Retrieve candidate by ID and delete from the database
    candidate = Candidate.query.get_or_404(candidate_id)
    db.session.delete(candidate)
    db.session.commit()
    flash('Candidate deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' in request.files:
        resume_file = request.files['resume']
        if resume_file.filename != '':
            filename = secure_filename(resume_file.filename)
            resume_content = resume_file.read().decode('utf-8')
            # Save resume to database
            user_id = 1  # Get user id from session or login
            new_resume = Resume(filename=filename, content=resume_content, user_id=user_id)
            db.session.add(new_resume)
            db.session.commit()
            # Analyze the resume
            analyze_resume(new_resume)
            flash('Resume uploaded successfully!', 'success')
    return redirect(url_for('user_dashboard'))

@app.route('/analyze_resume',methods=['POST'])
def analyze_resume(resume, job_requirements):
    # Parse the resume content
    text = resume.content
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    # Match skills with job requirements
    matched_skills, missing_skills = match_skills(filtered_tokens, job_requirements)
    # Calculate resume score
    calculate_resume_score = calculate_resume_score(filtered_tokens)
    # Save analysis results to database or display them on the user dashboard
    # (Implementation omitted for brevity)

def calculate_resume_score(tokens, job_requirements):
    # Calculate the score based on various factors such as keyword matching, experience, and education
    keyword_score = calculate_keyword_score(tokens, job_requirements)
    experience_score = calculate_experience_score(tokens)
    education_score = calculate_education_score(tokens)
    # Calculate the overall score as the average of individual scores
    overall_score = (keyword_score + experience_score + education_score) / 3
    return overall_score

def calculate_keyword_score(tokens, job_requirements):
    # Calculate the score based on keyword matching with job requirements
    # For demonstration purposes, let's simply count the number of matching keywords
    matching_keywords = [token for token in tokens if token.lower() in job_requirements]
    keyword_score = len(matching_keywords) / len(job_requirements) * 100
    return keyword_score

def calculate_experience_score(tokens):
    # Placeholder function to calculate the score based on relevant experience
    # For demonstration purposes, let's assume a higher score for resumes with more words related to experience
    experience_words = ['experience', 'skills', 'projects', 'work']
    num_experience_words = sum(1 for token in tokens if token.lower() in experience_words)
    experience_score = (num_experience_words / len(tokens)) * 100
    return experience_score

def calculate_education_score(tokens):
    # Placeholder function to calculate the score based on education level
    # For demonstration purposes, let's assume a higher score for resumes with mentions of education
    education_words = ['education', 'degree', 'university', 'college']
    num_education_words = sum(1 for token in tokens if token.lower() in education_words)
    education_score = (num_education_words / len(tokens)) * 100
    return education_score


def match_skills(tokens, job_requirements):
    # Match skills in the resume with the job requirements
    matched_skills = [token for token in tokens if token.lower() in job_requirements]
    # Identify missing skills by subtracting matched skills from job requirements
    missing_skills = [requirement for requirement in job_requirements if requirement.lower() not in matched_skills]
    return matched_skills, missing_skills


if __name__ == '__main__':
    with app.app_context():
     db.create_all()
    app.run(debug=True, port=5005)

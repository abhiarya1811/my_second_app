from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume_matching.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize SQLAlchemy database
db = SQLAlchemy(app)

# Import views to register routes
from app import routes
from app.views import user_views, job_views, admin_views

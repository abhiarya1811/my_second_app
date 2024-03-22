from flask import render_template, redirect, url_for, flash, request,session
from app import app, db
from app.models import Candidate, Job, Admin 


@app.route('/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        # Handle admin registration
        # Retrieve admin details from the form
        username = request.form['username']
        password = request.form['password']
        # Create a new admin instance
        new_admin = Admin(username=username, password=password)
        # Add the new admin to the database
        db.session.add(new_admin)
        db.session.commit()
        flash('Admin registered successfully!', 'success')
        return redirect(url_for('register'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # Handle admin login
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            # Admin login successful
            # Store admin session or use any authentication method
            session['admin_logged_in'] = True
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')




@app.route('/admin_dashboard')
def admin_dashboard():
    # Retrieve all candidates from the database
    candidates = Candidate.query.all()
    return render_template('admin_dashboard.html', candidates=candidates)

@app.route('/delete_candidate/<int:candidate_id>', methods=['POST'])
def delete_candidate(candidate_id):
    # Retrieve candidate by ID and delete from the database
    candidate = Candidate.query.get_or_404(candidate_id)
    db.session.delete(candidate)
    db.session.commit()
    flash('Candidate deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/post_job', methods=['GET', 'POST'])
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
    return render_template('post_job.html')

@app.route('/update_job/<int:job_id>', methods=['GET', 'POST'])
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    if request.method == 'POST':
        # Retrieve job details from form
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
    return render_template('update_job.html', job=job)

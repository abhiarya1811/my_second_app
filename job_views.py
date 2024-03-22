from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Job

# Define job-related views, such as posting, updating, and deleting jobs

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

@app.route('/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo, bcrypt, login_manager
from models import Student
import hmac

student_bp = Blueprint('student', __name__)

@student_bp.route('/signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password).decode('utf-8')
        new_student = Student(username=username, email=email, password=hashed_password)
        new_student.save_to_db()
        flash('Account created successfully!', 'success')
        return redirect(url_for('student.student_login'))
    return render_template('student_signup.html')

@student_bp.route('/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        student = Student.get_by_email(email)
        if student and hmac.compare_digest(student.password, password):
            login_user(student)
            flash('Login successful!', 'success')
            return redirect(url_for('student.student_dashboard'))
        else:
            flash('Login unsuccessful. Check email and password.', 'danger')
    return render_template('student_login.html')

@student_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def student_dashboard():
    if request.method == 'POST':
        room = request.form['room']
        current_user.room = room
        current_user.save_to_db()
        flash('Room selected successfully!', 'success')
    return render_template('student_dashboard.html', room=current_user.room)

@student_bp.route('/feedback', methods=['POST'])
@login_required
def student_feedback():
    feedback = request.form['feedback']
    current_user.feedback = feedback
    current_user.save_to_db()
    flash('Feedback submitted successfully!', 'success')
    return redirect(url_for('student.student_dashboard'))

@student_bp.route('/logout')
def student_logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('student.student_login'))

@login_manager.user_loader
def load_user(user_id):
    return Student.get_by_id(user_id)

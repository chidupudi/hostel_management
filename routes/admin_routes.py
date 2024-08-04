from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo, bcrypt, login_manager
from models import Admin
import hmac

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.get_by_username(username)
        if admin and hmac.compare_digest(admin.password, password):
            login_user(admin)
            flash('Login successful!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Login unsuccessful. Check username and password.', 'danger')
    return render_template('admin_login.html')

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    students = mongo.db.students.find()
    return render_template('admin_dashboard.html', students=students)

@admin_bp.route('/logout')
def admin_logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('admin.admin_login'))

@login_manager.user_loader
def load_user(user_id):
    return Admin.get_by_id(user_id)

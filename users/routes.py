from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db
from ..models import User
import hashlib

users_bp = Blueprint('users', __name__, template_folder='templates')

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email    = request.form['email']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'warning')
            return redirect(url_for('users.register'))
        user = User(username=username, email=email, password=hash_pw(password))
        db.session.add(user)
        db.session.commit()
        flash('Register successful!', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username'],
            password=hash_pw(request.form['password'])
        ).first()
        if user:
            login_user(user)
            return redirect(url_for('core.index'))
        flash('Username or Password is incorrect', 'warning')
    return render_template('users/login.html')

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users_bp.route('/profile')
@login_required
def profile():
    return render_template('users/profile.html', user=current_user)

@users_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_pw = hash_pw(request.form['old_password'])
        if current_user.password != old_pw:
            flash('Old password is incorrect', 'warning')
        else:
            current_user.password = hash_pw(request.form['new_password'])
            db.session.commit()
            flash('Password changed successfully', 'success')
    return render_template('users/change_password.html')
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from werkzeug.security import check_password_hash
from models.db import query

auth = Blueprint('auth', __name__)

# LOGIN REQUIRED DECORATOR (Isse baki admin pages secure rehte hain)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please login first.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# SECURE LOGIN ROUTE
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Database se user fetch kar rahe hain
        user = query("SELECT * FROM users WHERE email=%s", (email,), one=True)

        if user:
            # Handle dictionary or tuple connector type safely
            db_password = user['password'] if isinstance(user, dict) else user[3]
            db_id = user['id'] if isinstance(user, dict) else user[0]
            db_name = user['name'] if isinstance(user, dict) else user[1]
            db_role = user['role'] if isinstance(user, dict) else user[4]

            # Securely checking hashed password
            if check_password_hash(db_password, password):
                session['user_id'] = db_id
                session['user_name'] = db_name
                session['user_role'] = db_role

                flash('Login successful!', 'success')
                return redirect(url_for('admin.dashboard'))
        
        # Agar kuch galat ho toh generic error (security ke liye dono ka error same hona chahiye)
        flash('Invalid email or password.', 'danger')

    return render_template('login.html')

# LOGOUT ROUTE
@auth.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('public.home'))
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import db, bcrypt
from app.models import User
from app.forms import RegisterForm
from app.forms import LoginForm  # we'll create this too

auth_bp = Blueprint('auth', __name__, template_folder='templates')

# ─────────────────────────────
#  Register
# ─────────────────────────────
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print("✅ Form validated successfully!")
        print("Data received:", form.username.data, form.email.data)
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        print("💾 User committed to database!")
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    else:
        # This will show why the form didn’t validate
        print("❌ Form validation failed:", form.errors)

    return render_template('register.html', form=form)


# ─────────────────────────────
#  Login
# ─────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Welcome back!', 'success')
            return redirect(url_for('tasks.task_list'))
        flash('Invalid credentials. Try again.', 'danger')
    return render_template('login.html', form=form)

# ─────────────────────────────
#  Logout
# ─────────────────────────────
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
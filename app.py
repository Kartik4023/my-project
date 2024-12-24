from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
import calendar  # Make sure to import the calendar module

# from .models import Workout  # Use relative import if models.py is in the same folder

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:kartikmits@localhost/fitdatabase'

# Initialize CSRF protection
csrf = CSRFProtect(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


# Define the Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=45)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=255)])
    submit = SubmitField('Register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the email or username already exists
        existing_user = User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first()

        if existing_user:
            flash('User with this email or username already exists!', 'error')
            return redirect(url_for('register'))

        # Hash the password with bcrypt
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        try:
            # Add new user to the database
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username and password are provided
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return redirect(url_for('login'))

        # Fetch the user from the database
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = user.username
            session['user_id'] = user.id  # Store the user ID in the session

            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/home')
def home():
    # Check if the user is logged in
    if 'logged_in' not in session:
        flash('Please log in to access the home page.', 'error')
        return redirect(url_for('login'))
    return render_template('home.html')

import json

def load_users():
    # Load users from a JSON file
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
            return users
    except FileNotFoundError:
        print("Users file not found. Returning an empty dictionary.")
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON. Returning an empty dictionary.")
        return {}

def load_users():
    try:
        with open('users.json', 'r') as f:  # Adjust the path as necessary
            return json.load(f)
    except FileNotFoundError:
        return {}

# Example function to save users, replace with your actual implementation
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)



@app.route('/calendar/<int:year>/<int:month>')
def calendar_view(year=None, month=None):
    today = datetime.now().date()
    year = year or today.year
    month = month or today.month

    cal = calendar.Calendar(firstweekday=6)  # Sunday as the first day
    month_days = [day for day in cal.itermonthdates(year, month)]
    month_days = [day if day.month == month else None for day in month_days]  # Exclude other months

    prev_month = (year, month - 1) if month > 1 else (year - 1, 12)
    next_month = (year, month + 1) if month < 12 else (year + 1, 1)

    return render_template(
        'calendar.html',
        year=year,
        month=month,
        days=month_days,
        today=today,
        prev_month=prev_month,
        next_month=next_month,
        calendar=calendar
    )

import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your DB username
        password='kartikmits',  # Replace with your DB password
        database='fitdatabase'  # Replace with your DB name
    )
    return connection
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    body_part = db.Column(db.String(100), nullable=False)
    exercise = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User model

    def __init__(self, date, body_part, exercise, weight, reps, notes, user_id):
        self.date = date
        self.body_part = body_part
        self.exercise = exercise
        self.weight = weight
        self.reps = reps
        self.notes = notes
        self.user_id = user_id  # Associate workout with a specific user

@app.route('/workout', methods=['GET', 'POST'])
def workout():
    if request.method == 'POST':
        date = request.form.get('date')
        body_part = request.form.get('body_part')
        exercise = request.form.get('exercise')
        weight = request.form.get('weight')
        reps = request.form.get('reps')
        notes = request.form.get('notes')

        # Ensure all required fields are provided
        if not (date and body_part and exercise and weight and reps):
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('workout'))

        # Get the logged-in user's ID
        user_id = session.get('user_id')
        if not user_id:  # Ensure user is logged in
            flash('You must be logged in to add a workout.', 'error')
            return redirect(url_for('login'))  # Redirect to login if not logged in

        try:
            new_workout = Workout(
                date=datetime.strptime(date, '%Y-%m-%d'),
                body_part=body_part,
                exercise=exercise,
                weight=float(weight),
                reps=int(reps),
                notes=notes,
                user_id=user_id  # Assign the logged-in user's ID
            )
            db.session.add(new_workout)
            db.session.commit()
            flash('Workout added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding workout: {str(e)}', 'error')
        return redirect(url_for('workout'))

    return render_template('workout.html')

@app.route('/data_view')
def data_view():
    user_id = session.get('user_id')
    if not user_id:  # Ensure user is logged in
        flash('You must be logged in to view your data.', 'error')
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Get workouts for the logged-in user, ordered by date
    workouts = Workout.query.filter_by(user_id=user_id).order_by(Workout.date.desc()).all()
    return render_template('data.html', workouts=workouts)

@app.route('/delete_workout/<int:workout_id>', methods=['POST'])
def delete_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if workout:
        try:
            db.session.delete(workout)
            db.session.commit()
            flash('Workout deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting workout: {str(e)}', 'error')
    return redirect(url_for('data_view'))

@app.route('/workout')
def show_workouts():
    workouts = Workout.query.all()
    return render_template('data.html', workouts=workouts)


# Workout check route
@app.route('/workout-check')
def workout_check():
    return render_template('workoutcheck.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
 
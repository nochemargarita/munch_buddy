from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Like, Restaurant, Category, Message
import os

app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/signup')
def signup_form():
    """Directs user to a form."""
    
    return render_template("signup.html")

@app.route('/signup', methods=['POST'])
def signup():
    """Process signup using post request."""
    
    email = request.form.get('email')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    birthday = request.form.get('birthday')

    q = db.session.query(User).filter(User.email == email).first()

    if q:
        flash('Email is already taken.')
        return redirect('/signup')

    else:
        flash('Yay! You are now a Munch Buddy!')
        user = User(email=email, password=password, fname=fname, lname=lname, birthday=birthday)
        db.session.add(user)
        db.session.commit()
        return redirect('/')

@app.route('/login')
def login_form():
    """Let the use fill out login form."""

    return render_template('/login.html')

@app.route('/login', methods=['POST'])
def login():
    """Log the user in."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = db.session.query(User).filter(User.email == email, User.password == password).first()

    if user:
        session['email'] = email
        return redirect('/')

    else:
        flash('Please check your email and password!')
        return redirect('/login')


@app.route('/logout')
def logout():
    """Logs the user our from the session."""
    flash('You successfully logged out.')
    session.pop('email', None)
    return redirect('/')


@app.route('/categories')
def select_categories():
    """Let's the user select multiple categories of cuisine."""
    
    categories = Category.query.all()

    return render_template('/categories.html', categories=categories)

@app.route('/')
def result():
   pass 

if __name__ == "__main__":
    # set debug to True at the point of invoking the DebugToolbarExtension
    # app.debug = False

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

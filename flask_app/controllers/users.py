from flask_app import app, Bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User

from pprint import pprint

bcrypt = Bcrypt(app)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/register')
def register():
    if 'user_id' in session:
        return redirect('/')
    return render_template('register.html')
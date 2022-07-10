from flask_app import app, Bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.binder import Binder
from flask_app.models.user import User

from pprint import pprint

bcrypt = Bcrypt(app)

@app.route('/')
def landingpage():
    if 'user_id' in session:
        return redirect('/homepage')
    return render_template('landingpage.html')

# ~~~~~ GO TO REGISTER PAGE ~~~~~
@app.route('/register')
def register():
    if 'user_id' in session:
        return redirect('/')
    return render_template('register.html')


# ~~~~~ POST REQUEST FOR SAVING NEW USER ~~~~~
@app.route('/create_account', methods=['POST'])
def create_account():
    if not User.validate_user(request.form):
        return redirect('/register')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'username': request.form['username'],
        'email': request.form['email'],
        'password': pw_hash
    }

    user_id = User.save(data)
    pprint(user_id)
    session['user_id'] = user_id
    session['username'] = request.form['username']
    return redirect('/homepage')

# ~~~~~ GO TO LOGIN PAGE ~~~~~
@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')

# ~~~~~ POST REQUEST FOR SIGNING IN ~~~~~
@app.route('/sign_in', methods=['POST'])
def sign_in():
    data = { 
        "email" : request.form["email"]
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email")
        return redirect("/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/login')
    session['user_id'] = user_in_db.id
    session['username'] = user_in_db.username
    return redirect("/homepage")

# ~~~~~ LOG OUT ~~~~~
@app.route('/sign_out')
def sign_out():
    session.clear()
    return render_template('landingpage.html')

# ~~~~~ GO TO HOMEPAGE ~~~~~
@app.route('/homepage')
def homepage():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('homepage.html')

# ~~~~~ GO TO PROFILE PAGE ~~~~~
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    all_binders = Binder.get_all_binders()

    data = {
        'id': session['user_id']
    }
    current_user = User.get_by_id(data)
    
    return render_template('profile.html', all_binders = all_binders, current_user = current_user)

# ~~~~~ EDIT PROFILE INFO ~~~~~
@app.route('/about')
def edit_profile():
    if 'user_id' not in session:
        return redirect('/login')
    data = {
        'id': session['user_id']
    }
    current_user = User.get_by_id(data)

    return render_template('editprofile.html', current_user = current_user)

# ~~~~~ SAVE UPDATE ~~~~~
@app.route('/save_update', methods=['POST'])
def save_update():
    street_address = request.form['street']
    city = request.form['city']
    state = request.form['state']
    zipcode = request.form['zipcode']
    file = request.files['profile_icon']

    binary_image = file.read()

    address = street_address + ' ' + city + ', ' + state + ' ' + zipcode
    
    data = {
        'username': request.form['username'],
        'profile_icon': binary_image,
        'profile_bio': request.form['profile_bio'],
        'address': address,
        'id': session['user_id']
    }


    session['username'] = request.form['username']

    pprint(data)
    # User.update(data)

    return redirect('/profile')
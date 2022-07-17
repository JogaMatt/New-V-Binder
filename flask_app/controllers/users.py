from flask_app import app, Bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.binder import Binder
from flask_app.models.message import Message
from flask_app.models.user import User
from flask_app.models.friend import Friend

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
    # all_binders = Binder.get_all_binders()

    data = {
        'id': session['user_id']
    }
    my_binders = Binder.get_current_users_binders(data)
    current_user = User.get_by_id(data)

    data = {
        'receiver_id': session['user_id']
    }
    my_messages = Message.get_my_messages(data)
    
    data = {
        'id': session['user_id']
    }
    friends = Friend.get_my_friends(data)
    requests = Friend.get_my_requests(data)
    pprint(friends)
    
    return render_template('profile.html', my_binders = my_binders, current_user = current_user, my_messages = my_messages, friends = friends, requests = requests)

# ~~~~~ GO TO OTHER USER'S PROFILE ~~~~~
@app.route('/profile/<id>')
def other_profile(id):
    data = {
        'id': id
    }
    user = User.get_by_id(data)
    binders = Binder.get_current_users_binders(data)
    friends = Friend.get_my_friends(data)
    
    data = {
        'id_one': session['user_id'],
        'id_two': id
    }
    friend_check = Friend.friend_check(data)
    # print(friend_check)
    return render_template('other_profile.html', user = user, binders = binders, friends = friends, friend_check = friend_check)

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

    address = street_address + ' ' + city + ', ' + state + ' ' + zipcode
    
    data = {
        'username': request.form['username'],
        'profile_icon': request.form['profile_icon'],
        'address': address,
        'id': session['user_id']
    }


    session['username'] = request.form['username']

    # pprint(data)
    User.update(data)

    return redirect('/profile')
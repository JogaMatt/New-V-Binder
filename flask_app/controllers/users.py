from itertools import product
import json
from flask_app import app, Bcrypt, stripe
from flask import render_template,redirect,request,session,flash,url_for
from flask_app.models.binder import Binder
from flask_app.models.message import Message
from flask_app.models.user import User
from flask_app.models.friend import Friend
from pprint import pprint

bcrypt = Bcrypt(app)

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51LNI6ACh5HPOp3tbdJKcRoWH2cvWqZWn9FMK7j4tGTlCgHK8mcg7mXWFqrg0jxjlZTsZQX8VBItlKzWciAe3TAuv00w8kzrh25'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51LNI6ACh5HPOp3tb8ggo5YoHdI5bTNmTn9aBYQcNIcjb4KmiD8a5psrIOa2Jto2jxGOVo5fBJGUCgab0kohH9bg300Nlju5261'

stripe.api_key = app.config['STRIPE_SECRET_KEY']

def cart():
    cart = session['cart']
    return cart

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

# ~~~~~ GO TO MARKETPLACE ~~~~~
@app.route('/shop')
def shop():

    products = [{
        'product_image': 'https://images.pokemontcg.io/swsh7/215_hires.png',
        'product_name': 'Umbreon VMAX (Alternate Art)',
        'product_id': 'prod_M5TNNnnbO0mRpR',
        'price': 'price_1LNIQbCh5HPOp3tbwt8HWoZo'
    }]
    return render_template('marketplace.html', products = products)

# ~~~~~ ADD TO CART ~~~~~
@app.route('/add_cart', methods = ['POST'])
def add_cart():

    def  array_merge(arr1, arr2):
        return arr1 + arr2
    
    product = [{
        # 'product_image': request.form['product_image'],
        'price': request.form['price'],
        'adjustable_quantity': {
            'enabled': True,
            'minimum': 1,
            'maximum': 10,
        },
        'quantity': 1
    }]
    if 'cart' not in session:
        session['cart'] = product
    else:
        session['cart'] = array_merge(session['cart'], product)
    pprint(session['cart'])

    


    return redirect('/shop')

# ~~~~~ STRIPE PAY ~~~~~
@app.route('/stripe_pay')
def stripe_pay():
    cart_items = cart()
    pprint(cart_items)
    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items = cart_items,
        mode = 'payment',
        success_url = url_for('profile', _external = True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url = url_for('shop', _external = True)
    )
    return {
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY'],
        'checkout_session_id': session['id']
    }
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.card import Card
from flask_app.models.binder import Binder

@app.route('/create_binder')
def create_binder():
    if 'user_id' not in session:
        return redirect('/homepage')
    return render_template('create_binder.html')

@app.route('/save_binder', methods=['POST'])
def save_binder():
    data = {
        'name': request.form['name'],
        'trade': request.form['trade'],
        'user_id': session['user_id']
    }

    Binder.save(data)
    return redirect('/homepage')
from flask_app import app
from flask import current_app, render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.card import Card
from flask_app.models.binder import Binder
from pprint import pprint

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

# ~~~~~ VIEW CONTENTS OF BINDER ~~~~~
@app.route('/binder/<binder_id>')
def view_binder(binder_id):
    if 'user_id' not in session:
        return redirect('/login')

    data = {
        'id': binder_id
    }

    current_binder = Binder.get_one(data)
    session['binder_id'] = current_binder[0]['binder_id']

    return render_template('mybinder.html', current_binder = current_binder)
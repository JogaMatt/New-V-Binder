from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.card import Card

from pprint import pprint

# ~~~~~ SEARCH FOR A CARD ~~~~~
@app.route('/search_card', methods=['POST'])
def search_card():
    search_term = request.form['search-bar'].replace(' ', '*')
    return redirect(f'/search/{search_term}')

@app.route('/search/<name>')
def search_results(name):
    cards = Card.get_all(name)
    # pprint(cards['data'][0]['id'])
    return render_template('search.html', cards = cards['data'], search = name.replace('*', ' '))

from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.card import Card

from pprint import pprint

# ~~~~~ SEARCH FOR A CARD ~~~~~
@app.route('/search_card', methods=['POST'])
def search_card():
    search_term = request.form['search-bar'].replace(' ', '*')
    return redirect(f'/search/{search_term}/1')

# ~~~~~ PASS SEARCHED CARD TO SEARCH PAGE ~~~~~
@app.route('/search/<name>/<page>')
def search_results(name, page):
    all_cards_in_api = Card.get_all(name)
    cards = Card.get_15(name, page)
    current_page = int(page)

    return render_template('search.html', cards = cards['data'], current_page = current_page, all_cards = all_cards_in_api['data'], search = name.replace('*', ' '))

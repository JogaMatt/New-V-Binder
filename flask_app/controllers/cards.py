from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.card import Card
from flask_app.models.binder import Binder

from pprint import pprint

# ~~~~~ SEARCH FOR A CARD ~~~~~
@app.route('/search_card', methods=['POST'])
def search_card():
    search_term = request.form['search-bar'].replace(' ', '*')
    return redirect(f'/search/{search_term}/1')

# ~~~~~ PASS SEARCHED CARD TO SEARCH PAGE ~~~~~
@app.route('/search/<name>/<page>')
def search_results(name, page):
    if 'user_id' not in session:
        return redirect('/homepage')
    all_cards_in_api = Card.get_all(name)
    cards = Card.get_15(name, page)
    current_page = int(page)

    return render_template('search.html', cards = cards['data'], current_page = current_page, all_cards = all_cards_in_api['data'], search = name.replace('*', ' '))

# ~~~~~ BROWSE ALL AVAILABLE EXPANSIONS ~~~~~
@app.route('/expansions/<page>')
def expansions(page):
    all_expansions = Card.get_all_sets(page)
    pprint(all_expansions['data'])
    return render_template('expansions.html', all_expansions = all_expansions['data'])

# ~~~~~ CARD DETAIL PAGE ~~~~~
@app.route('/details/<id>')
def card_details(id):
    card = Card.get_one(id)
    pprint(card['data'])
    all_binders = Binder.get_all_binders()

    data = {
        'id': session['user_id']
    }

    current_users_binders = Binder.get_current_users_binders(data)
    return render_template('carddetails.html', card = card['data'], all_binders = all_binders, my_binders = current_users_binders)

# ~~~~~ SAVE CARD TO BINDER ~~~~~
@app.route('/save_card', methods=['POST'])
def save_to_binder():
    pprint(request.form)
    if not Card.validate_save(request.form):
        return redirect(f"/details/{request.form['card_id']}")

    data = {
        'name': request.form['name'],
        'card_condition': request.form['card_condition'],
        'image_address': request.form['image_address'],
        'card_id': request.form['card_id'],
        'binder_id': request.form['binder_id']
    }

    quantity = request.form['quantity']
    pprint(quantity)

    for x in range(0, int(quantity)):
        Card.save(data)

    session['binder_id'] = request.form['binder_id']

    return redirect('/homepage')
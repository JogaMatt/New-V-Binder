from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re, requests
from flask_app.models.user import User

DATABASE = 'my_v_binder'

class Card:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.card_condition = data['card_condition']
        self.image_address = data['image_address']
        self.card_id = data['card_id']
        self.binder_id = data['binder_id']

    @classmethod
    def save(cls, data:dict ) -> int:
        query = "INSERT INTO cards (name, card_condition, image_address, card_id, binder_id) VALUES ( %(name)s, %(card_condition)s, %(image_address)s, %(card_id)s, %(binder_id)s);"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM cards WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_one_with_users(cls, data):
        query  = "SELECT * FROM cards LEFT JOIN binders ON cards.binder_id = binders.id LEFT JOIN users ON binders.user_id = users.id WHERE cards.card_id = %(id)s and binders.trade = 'true';"
        results = connectToMySQL(DATABASE).query_db(query, data)
        # pprint(results)
        users = []
        for result in results:
            cardHolder_data = {
                'id' : result['users.id'],
                'first_name' : result['first_name'],
                'last_name' : result['last_name'],
                'username' : result['username'],
                'address': result['address'],
                'profile_icon': result['profile_icon'],
                'profile_bio': result['profile_bio'],
                'email' : result['email'],
                'password' : result['password'],
                'created_at' : result['users.created_at'],
                'updated_at' : result['updated_at']
            }
            users.append(User(cardHolder_data))
        # pprint(users)
        return users

    @classmethod
    def get_one_with_users_new(cls, data):
        query  = "SELECT * FROM cards LEFT JOIN binders ON cards.binder_id = binders.id LEFT JOIN users ON binders.user_id = users.id WHERE cards.id = %(id)s and binders.trade = 'true';"
        results = connectToMySQL(DATABASE).query_db(query, data)
        # pprint(results)
        users = []
        for result in results:
            cardHolder_data = {
                'id' : result['users.id'],
                'first_name' : result['first_name'],
                'last_name' : result['last_name'],
                'username' : result['username'],
                'address': result['address'],
                'profile_icon': result['profile_icon'],
                'profile_bio': result['profile_bio'],
                'email' : result['email'],
                'password' : result['password'],
                'created_at' : result['users.created_at'],
                'updated_at' : result['updated_at']
            }
            users.append(cardHolder_data)
        # pprint(users)
        return users

    @classmethod
    def public_trades(cls):
        query = "SELECT * FROM cards LEFT JOIN binders ON cards.binder_id = binders.id LEFT JOIN users ON binders.user_id = users.id WHERE binders.trade = 'true' ORDER BY cards.id DESC;"
        results = connectToMySQL(DATABASE).query_db(query)
        # pprint(results)
        cards = []
        for result in results:
            card_data = {
                'id': result['id'],
                'name': result['name'],
                'card_condition': result['card_condition'],
                'image_address': result['image_address'],
                'card_id': result['card_id'],
                'binder_id': result['binder_id'],
                'username': result['username'],
                'profile_icon': result['profile_icon'],
                'user_id': result['user_id']
            }
            cards.append(card_data)
        # pprint(cards)
        return cards

    @classmethod
    def search_trade_list(cls, data):
        query = "SELECT * FROM cards LEFT JOIN binders ON cards.binder_id = binders.id LEFT JOIN users ON binders.user_id = users.id WHERE cards.name = %(name)s and binders.trade = 'true' ORDER BY cards.id DESC"
        results = connectToMySQL(DATABASE).query_db(query, data)
        # pprint(results)
        cards = []
        for result in results:
            card_data = {
                'id': result['id'],
                'name': result['name'],
                'card_condition': result['card_condition'],
                'image_address': result['image_address'],
                'card_id': result['card_id'],
                'binder_id': result['binder_id'],
                'username': result['username'],
                'profile_icon': result['profile_icon'],
                'user_id': result['user_id']
            }
            cards.append(card_data)
        return cards


    @classmethod
    def get_my_cards(cls, data):
        query = "SELECT * FROM cards WHERE binder_id = %(binder_id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        cards = []
        for row in results:
            cards.append( cls(row) )
        return cards

    @classmethod
    def get_all(cls, name):
        response = requests.get(f"https://api.pokemontcg.io/v2/cards?q=name:{name}")
        return response.json()

    @classmethod
    def get_15(cls, name, page):
        response = requests.get(f"https://api.pokemontcg.io/v2/cards?q=name:{name}&page={page}&pageSize=15")
        return response.json()

    @classmethod
    def get_all_sets(cls, page):
        response = requests.get(f"https://api.pokemontcg.io/v2/sets?page={page}&pageSize=30")
        return response.json()

    @classmethod
    def get_one(cls, id):
        response = requests.get(f"https://api.pokemontcg.io/v2/cards/{id}")
        pprint(response)
        return response.json()

    @classmethod
    def get_one_from_db(cls, data):
        query = "SELECT * FROM cards WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        card = []
        for result in results:
            card_data = {
                'id': result['id'],
                'name': result['name'],
                'card_condition': result['card_condition'],
                'image_address': result['image_address'],
                'card_id': result['card_id'],
                'binder_id': result['binder_id']
            }
            card.append(card_data)
        return card


    @staticmethod
    def validate_save(card:dict) -> bool:
        # pprint(card)
        is_valid = True # ! we assume this is true
        if(card['binder_id'] == "0"):
            flash("Must select a binder!")
            is_valid = False
        if(card['card_condition'] == "0"):
            flash("Must select a card condition!")
            is_valid = False
        if(card['quantity'] == ""):
            flash("Must select a quantity!")
            is_valid = False
        return is_valid
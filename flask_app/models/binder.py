from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from pprint import pprint

DATABASE = 'my_v_binder'

class Binder:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.trade = data['trade']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data:dict ) -> int:
        query = "INSERT INTO binders (name, trade, user_id) VALUES ( %(name)s, %(trade)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def update(cls,data):
        query = "UPDATE binders SET card_id=%(card_id)s, updated_at=NOW() WHERE user_id = %(user_id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_all_binders(cls):
        query = "SELECT * FROM binders;"
        results = connectToMySQL(DATABASE).query_db(query)
        binders = []
        for row in results:
            binders.append( cls(row) )
        return binders

    @classmethod
    def get_current_users_binders(cls, data):
        query = "SELECT * FROM binders WHERE user_id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        pprint(results)
        binders = []
        for row in results:
            binders.append( cls(row) )
        return binders

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM binders LEFT JOIN cards ON binders.id = cards.binder_id WHERE binders.id = %(id)s";
        results = connectToMySQL(DATABASE).query_db(query,data)
        cards = []
        for result in results:
            # pprint(result)
            data = {
                'binder_id': result['binder_id'],
                'card_condition': result['card_condition'],
                'card_id': result['card_id'],
                'cards_id': result['cards.id'],
                'cards_name': result['cards.name'],
                'id': result['id'],
                'image_address': result['image_address'],
                'name': result['name'],
                'trade': result['trade'],
                'user_id': result['user_id']
            }
            cards.append(data)
        return cards
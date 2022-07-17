from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from pprint import pprint

DATABASE = 'my_v_binder'

class Friend:
    def __init__( self , data ):
        self.id = data['id']
        self.request_approval = data['request_approval']
        self.request_sender_id = data['request_sender_id']
        self.request_sender_name = data['request_sender_name']
        self.request_receiver_id = data['request_receiver_id']
        self.request_receiver_name = data['request_receiver_name']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data:dict ) -> int:
        query = "INSERT INTO friends (request_approval, request_sender_id, request_sender_name, request_receiver_id, request_receiver_name, user_id) VALUES ( %(request_approval)s, %(request_sender_id)s, %(request_sender_name)s, %(request_receiver_id)s, %(request_receiver_name)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def update(cls,data):
        query = "UPDATE friends SET request_approval=%(request_approval)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)


    @classmethod
    def delete(cls,data):
        query = "DELETE FROM friends WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_all_friends(cls):
        query = "SELECT * FROM friends;"
        results = connectToMySQL(DATABASE).query_db(query)
        friends = []
        for row in results:
            friends.append( cls(row) )
        return friends

    @classmethod
    def get_my_friends(cls, data):
        query = "SELECT * FROM friends WHERE request_receiver_id = %(id)s AND request_approval = 'approved' OR request_sender_id = %(id)s AND request_approval = 'approved';"
        results = connectToMySQL(DATABASE).query_db(query, data)
        friends = []
        for row in results:
            friends.append( cls(row) )
        return friends

    @classmethod
    def get_my_requests(cls, data):
        query = "SELECT * FROM friends WHERE request_approval = 'pending' AND request_receiver_id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        requests = []
        for row in results:
            requests.append( cls(row) )
        return requests

    @classmethod
    def friend_check(cls, data):
        query = "SELECT * FROM friends WHERE request_receiver_id = %(id_one)s AND request_sender_id = %(id_two)s AND request_approval = 'approved' OR request_receiver_id = %(id_two)s AND request_sender_id = %(id_one)s AND request_approval = 'approved'"
        result = connectToMySQL(DATABASE).query_db(query, data)
        # pprint(result)
        friends = []
        for row in result:
            friends.append( cls(row) )
        if len(friends) == 0:
            friends.append('pending')
        return friends
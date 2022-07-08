from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from pprint import pprint

DATABASE = 'my_v_binder'

class Message:
    def __init__( self , data ):
        self.id = data['id']
        self.message_info = data['message_info']
        self.sender_id = data['sender_id']
        self.sender_name = data['sender_name']
        self.receiver_id = data['receiver_id']
        self.created_at = data['created_at']
        self.update_at = data['update_at']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data:dict ) -> int:
        query = "INSERT INTO messages (message_info, sender_id, sender_name, receiver_id, user_id) VALUES ( %(message_info)s, %(sender_id)s, %(sender_name)s, %(receiver_id)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM messages WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_all_messages(cls):
        query = "SELECT * FROM messages;"
        results = connectToMySQL(DATABASE).query_db(query)
        messages = []
        for row in results:
            messages.append( cls(row) )
        return messages
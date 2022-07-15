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
        self.chat_id = data['chat_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (message_info, sender_id, sender_name, receiver_id, chat_id) VALUES ( %(message_info)s, %(sender_id)s, %(sender_name)s, %(receiver_id)s, %(chat_id)s );"
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

    @classmethod
    def messages_in_chat(cls, data):
        query = "SELECT * FROM messages LEFT JOIN chats ON messages.chat_id = chats.id LEFT JOIN users ON chats.user_id = users.id WHERE messages.chat_id = %(chat_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        messages = []
        for result in results:
            message_data = {
            'id': result['id'],
            'message_info': result['message_info'],
            'sender_id': result['sender_id'],
            'sender_name': result['sender_name'],
            'receiver_id': result['receiver_id'],
            'created_at': result['created_at'],
            'update_at': result['update_at'],
            'chat_id': result['chat_id']
            }
            messages.append(message_data)
        # pprint(messages[0])
        return messages

    @classmethod
    def get_my_messages(cls, data):
        query = "SELECT * FROM messages WHERE receiver_id = %(receiver_id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        messages = []
        for row in results:
            messages.append(cls(row))
        return messages
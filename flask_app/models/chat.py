from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from pprint import pprint

DATABASE = 'my_v_binder'

class Chat:
    def __init__(self, data):
        self.id = data['id']
        self.chat_name = data['chat_name']
        self.chat_sender_name = data['chat_sender_name']
        self.chat_receiver_id = data['chat_receiver_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO chats (chat_name, chat_sender_name, chat_receiver_id, user_id) VALUES ( %(chat_name)s, %(chat_sender_name)s, %(chat_receiver_id)s, %(user_id)s );"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def all_chats(cls):
        query = "SELECT * FROM chats;"
        results = connectToMySQL(DATABASE).query_db(query)
        chats = []
        for chat in results:
            chats.append( cls(chat) )
        return chats

    @classmethod
    def last_chat(cls):
        query = "SELECT * FROM chats ORDER BY id DESC LIMIT 1;"
        result = connectToMySQL(DATABASE).query_db(query)
        chat = []
        for row in result:
            chat.append(row)
        return chat

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM chats WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
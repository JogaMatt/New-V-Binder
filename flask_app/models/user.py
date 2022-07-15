from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from pprint import pprint
from flask_app.models.binder import Binder
from flask_app.models.message import Message
from flask_app.models.friend import Friend

DATABASE = 'my_v_binder'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.profile_icon = data['profile_icon']
        self.profile_bio = data['profile_bio']
        self.address = data['address']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.binders = []
        self.messages = []

    @classmethod
    def save(cls, data:dict ) -> int:
        query = "INSERT INTO users (first_name, last_name, username, email, password) VALUES ( %(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET username=%(username)s, profile_icon=%(profile_icon)s, address=%(address)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

        ## ! used in user validation
    @classmethod
    def get_by_id(cls,data:dict):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_email(cls,data:dict):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM users LEFT JOIN binders ON users.id = binders.user_id WHERE users.id = %(id)s";
        results = connectToMySQL(DATABASE).query_db(query,data)
        # pprint(results)
        user = cls(results[0])
        for result in results:
            # pprint(result)
            binder_data = {
                'id': result['binders.id'],
                'name': result['name'], 
                'trade': result['trade'],
                'user_id': result['user_id'],
                'created_at': result['binders.created_at'],
                'updated_at': result['binders.updated_at']
            }
            user.binders.append(Binder(binder_data))
        # pprint(user.binders)
        return user

    @classmethod
    def get_one_friends(cls,data):
        query  = "SELECT * FROM users LEFT JOIN friends ON users.id = friends.user_id WHERE users.id = %(id)s";
        results = connectToMySQL(DATABASE).query_db(query,data)
        # pprint(results)
        user = cls(results[0])
        for result in results:
            # pprint(result)
            friend_data = {
                'id': result['friends.id'],
                'request_approval': result['request_approval'],
                'request_sender_name': result['request_sender_name'],
                'request_sender_id': result['request_sender_id'],
                'request_receiver_name': result['request_receiver_name'],
                'request_receiver_id': result['request_receiver_id'],
                'user_id': result['user_id']
            }
            user.friends.append(Friend(friend_data))
        # pprint(user.binders)
        return user

    @classmethod
    def get_one_messages(cls,data):
        query  = "SELECT * FROM users LEFT JOIN messages ON users.id = messages.user_id WHERE users.id = %(id)s";
        results = connectToMySQL(DATABASE).query_db(query,data)
        # pprint(results)
        user = cls(results[0])
        for result in results:
            # pprint(result)
            message_data = {
                'id': result['messages.id'],
                'context': result['context'], 
                'sender_id': result['sender_id'],
                'receiver_id': result['receiver_id'],
                'user_id': result['user_id'],
                'created_at': result['binders.created_at'],
                'updated_at': result['binders.updated_at']
            }
            user.messages.append(Message(message_data))
        pprint(user.messages)
        return user

    @classmethod
    def get_one_user(cls,data):
        query  = "SELECT * FROM users WHERE id = %(id)s";
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for row in results:
            users.append( cls(row) )
        return users

    @staticmethod
    def validate_update(user:dict):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid


    @staticmethod
    def validate_user(user:dict):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("*First name must be at least 3 characters*")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("*Last name must be at least 3 characters*")
            is_valid = False
        if len(user['username']) < 5:
            flash("*Username must be at least 5 characters*")
            is_valid = False
        if len(user['password']) < 8:
            flash("*Password must be at least 8 characters*")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("*Invalid email address!*")
            is_valid = False
        if user['password'] != user['confirm-password']:
            flash("*Please enter matching passwords!*")
            is_valid = False
        return is_valid
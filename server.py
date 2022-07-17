from flask_app import app
from flask_app.controllers import users, cards, binders, messages, chats, friends

if __name__ == "__main__":
    app.run(debug=True)
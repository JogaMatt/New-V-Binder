from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.card import Card
from flask_app.models.binder import Binder
from flask_app.models.message import Message
from flask_app.models.chat import Chat
from pprint import pprint

# ~~~~~ RENDER MESSAGE FORM ~~~~~
@app.route('/message/<user_id>/<card_id>')
def inquiry_card(user_id, card_id):
    if 'user_id' not in session:
        return redirect('/login')
    data = {
        'id': user_id
    }
    receiver = User.get_by_id(data)

    data = {
        'id': card_id
    }
    current_card = Card.get_one_from_db(data)
    pprint(current_card)
    current_chat = Chat.last_chat()
    pprint(current_chat)
    return render_template('message.html', receiver = receiver, current_card = current_card[0], current_chat = current_chat[0])

# ~~~~~ SEND MESSAGE ~~~~~
@app.route('/send_message', methods = ['POST'])
def send_message():

    # pprint(request.form)

    Message.save(request.form)
    return redirect('/profile')

# ~~~~~ READ MESSAGES ~~~~~
@app.route('/messages')
def messages():
    if 'user_id' not in session:
        return redirect('/login')
    all_chats = Chat.all_chats()
    return render_template('mymessages.html', all_chats = all_chats)

# ~~~~~ REPLY TO MESSAGE ~~~~~
@app.route('/reply', methods = ['POST'])
def reply():
    Message.save(request.form)
    chat_id = request.form['chat_id']
    return redirect(f'/chat/{chat_id}')

# ~~~~~ DELETE MESSAGE ~~~~~
@app.route('/delete_message/<id>')
def delete_message(id):
    if 'user_id' not in session:
        flash("Please sign in/register")
        return redirect('/')
    data = {
        "id": id
    }
    Message.delete(data)
    return redirect('/messages')
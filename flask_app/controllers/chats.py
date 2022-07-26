from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.card import Card
from flask_app.models.binder import Binder
from flask_app.models.message import Message
from flask_app.models.chat import Chat
from pprint import pprint

@app.route('/create_chat/<user_id>/<card_id>', methods = ['POST'])
def create_chat(user_id, card_id):
    data = {
        'chat_name': request.form['chat_name'],
        'chat_sender_name': session['username'],
        'chat_receiver_id': request.form['chat_receiver_id'],
        'user_id': session['user_id']
    }

    Chat.save(data)
    return redirect(f'/message/{user_id}/{card_id}')

# ~~~~~ OPEN CHAT ~~~~~
@app.route('/chat/<chat_id>')
def open_chat(chat_id):
    data = {
        'chat_id': chat_id
    }
    current_chat = Message.messages_in_chat(data)

    if session['user_id'] == current_chat[0]['sender_id'] or session['user_id'] == current_chat[0]['receiver_id']:
        return render_template('chat.html', current_chat = current_chat)
    else:
        return redirect('/profile')
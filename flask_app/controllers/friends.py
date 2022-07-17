from flask_app import app, Bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.friend import Friend


from pprint import pprint

# ~~~~~ SEND REQUEST ~~~~~
@app.route('/send_request', methods=['POST'])
def send_request():
    pprint(request.form)
    id = request.form['request_receiver_id']
    Friend.save(request.form)
    return redirect(f'/profile/{id}')

# ~~~~~ RENDER REQUEST PAGE ~~~~~
@app.route('/friends/requests/<id>')
def my_requests(id):
    data = {
        'id': id
    }
    requests = Friend.get_my_requests(data)
    return render_template('myrequests.html', requests = requests)

# ~~~~~ APPROVE TO REQUEST ~~~~~
@app.route('/approve/<id>')
def approve_request(id):
    data = {
        'request_approval': 'approved',
        'id': id
    }
    Friend.update(data)
    user_id = session['user_id']
    return redirect(f'/friends/requests/{user_id}')

@app.route('/delete_request/<id>')
def delete_request(id):
    if 'user_id' not in session:
        flash("Please sign in/register")
        return redirect('/')
    data = {
        "id": id
    }
    Friend.delete(data)
    return redirect('/profile')
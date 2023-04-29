from flask import Flask, request, jsonify
from classes.userManager import UserManager
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)



@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if UserManager.login(username, password):
            user = UserManager.get_user(username)
            login_user(user)
            return jsonify({'status': 'login successful', 'mail': user.mail, 'nombre': user.nombre, 'emails': user.emails})
        else:
            return jsonify({'status': 'login failed'})

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if UserManager.get_user(username) is None:
            UserManager.add_user(username, password)
            return jsonify({'status': 'register successful'})
        else:
            return jsonify({'status': 'register failed'})
        
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        return jsonify({'status': 'logout successful'})
    
@app.route('/buzon', methods=['GET'])
@login_required
def buzon():
    if request.method == 'GET':
        return jsonify({'status': 'buzon successful', 'mail': current_user.mail, 'nombre': current_user.nombre, 'emails': current_user.emails})
    
@app.route('/send', methods=['POST'])
@login_required
def send():
    if request.method == 'POST':
        mail = request.form['mail']
        subject = request.form['subject']
        body = request.form['body']
        if UserManager.get_user_by_mail(mail) is not None:
            UserManager.get_user_by_mail(mail).add_email(mail, subject, body)
            return jsonify({'status': 'send successful'})
        else:
            return jsonify({'status': 'send failed'})
        
@app.route('/buzon/sort', methods=['POST'])
@login_required
def sort():
    if request.method == 'POST':
        sort = request.form['sort']
        if sort == 'date':
            current_user.sort_emails_by_date()
        elif sort == 'sender':
            current_user.sort_emails_by_sender()
        elif sort == 'subject':
            current_user.sort_emails_by_subject()
        return jsonify({'status': 'sort successful', 'mail': current_user.mail, 'nombre': current_user.nombre, 'emails': current_user.emails})
    
@app.route('/buzon/delete', methods=['POST'])
@login_required
def delete():
    if request.method == 'POST':
        index = request.form['index']
        current_user.delete_email(index)
        return jsonify({'status': 'delete successful', 'mail': current_user.mail, 'nombre': current_user.nombre, 'emails': current_user.emails})
    
@app.route('/buzon/read', methods=['POST'])
@login_required
def read():
    if request.method == 'POST':
        index = request.form['index']
        current_user.read_email(index)
        return jsonify({'status': 'read successful', 'mail': current_user.mail, 'nombre': current_user.nombre, 'emails': current_user.emails})
    
@app.route('/buzon/unread', methods=['POST'])
@login_required
def unread():
    if request.method == 'POST':
        index = request.form['index']
        current_user.unread_email(index)
        return jsonify({'status': 'unread successful', 'mail': current_user.mail, 'nombre': current_user.nombre, 'emails': current_user.emails})
    

        


if __name__ == '__main__':
    app.run(debug=True, port=4000)
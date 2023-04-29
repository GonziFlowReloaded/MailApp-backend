from flask import Flask, request, jsonify
from classes.userManager import UserManager
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from classes.user import Users
import os

app = Flask(__name__)
login_manager_app = LoginManager(app)
app.secret_key = os.urandom(12)
user_manager = UserManager()
user_manager.add_user(Users('usuario1', 'contraseña1'))
user_manager.add_user(Users('usuario2', 'contraseña2'))
        




@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        request_data = request.get_json()
        username = request_data['username']
        password = request_data['password']
        if user_manager.login(username, password):
            user = user_manager.get_user(username)
            login_user(user)
            return jsonify({'status': 'login successful', 'mail': user.mail, 'nombre': user.nombre, 'emails': user.emails})
        else:
            return jsonify({'status': 'login failed'})

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        request_data = request.get_json()
        username = request_data['username']
        password = request_data['password']
        if user_manager.get_user(username) is None:
            user_manager.add_user(username, password)
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
        request_data = request.get_json()
        mail = request_data['mail']
        subject = request_data['subject']
        body = request_data['body']
        if user_manager.get_user_by_mail(mail) is not None:
            user_manager.get_user_by_mail(mail).add_email(mail, subject, body)
            return jsonify({'status': 'send successful'})
        else:
            return jsonify({'status': 'send failed'})
        
@app.route('/buzon/sort', methods=['POST'])
@login_required
def sort():
    if request.method == 'POST':
        request_data = request.get_json()
        sort = request_data['sort']
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
        request_data = request.get_json()
        index = request_data['index']
        current_user.delete_email(index)
        return jsonify({'status': 'delete successful', 'mail': current_user.mail, 'nombre': current_user.nombre, 'emails': current_user.emails})
    
@app.route('/buzon/read', methods=['POST'])
@login_required
def read():
    if request.method == 'POST':
        request_data = request.get_json()
        index = request_data['index']
        current_user.read_email(index)
        return jsonify({'status': 'read successful', 'mail': current_user.mail, 'nombre': current_user.nombre, 'emails': current_user.emails})
    
@app.route('/buzon/unread', methods=['POST'])
@login_required
def unread():
    if request.method == 'POST':
        request_data = request.get_json()
        index = request_data['index']
        current_user.unread_email(index)
        return jsonify({'status': 'unread successful', 'mail': current_user.mail, 'nombre': current_user.nombre, 'emails': current_user.emails})
    


if __name__ == '__main__':
    app.run(debug=True, port=4000)
from flask import Flask, request, jsonify
from api.classes.userManager import UserManager
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from api.classes.user import Users
import os
from api.classes.email import Email
from api.classes.sortStrategy import SortByDate, SortBySender, SortBySubject, SortByReaded

app = Flask(__name__)
login_manager_app = LoginManager(app)
app.secret_key = os.urandom(12)
user_manager = UserManager()
user_manager.add_user(Users('usuario1', 'contraseña1'))
user_manager.add_user(Users('usuario2', 'contraseña2'))

        
@login_manager_app.user_loader
def load_user(user_id):
    return user_manager.users[int(user_id)]

@app.route('/', methods=['GET'])
def index():
    return 'Hello World'

    
#----------------------------------------------Login--------------------------------------------------------------#

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        request_data = request.get_json()
        username = request_data['username']
        password = request_data['password']
        if user_manager.login(username, password):
            
            user = user_manager.get_user(username)
            login_user(user)
            return jsonify({'status': 'login successful', 'mail': user.mail, 'nombre': user.nombre})
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
        userActual = current_user.mail
        logout_user()
        return jsonify({'status': 'logout successful', 'user': userActual})


#----------------------------------------------Buzon--------------------------------------------------------------#
@app.route('/buzon', methods=['GET'])
@login_required
def buzon():
    if request.method == 'GET':
        lista = []
        for mail in current_user.emails:
            mail_data = {'sender': mail.sender, 'subject': mail.subject, 'body': mail.body, 'date': mail.date, 'readed': mail.readed, 'id': mail.id}
            lista.append(mail_data)
        response_data = {'status': 'buzon successful', 'mail': current_user.mail, 'nombre': current_user.nombre, 'emails': lista}
        return jsonify(response_data)
    

@app.route('/buzon/<int:id>', methods=['GET'])
@login_required
def buzon_mail(id):
    if request.method == 'GET':
        current_user.emails[id].setReaded()
        mail = current_user.emails[id]
        mail_data = {'sender': mail.sender, 'subject': mail.subject, 'body': mail.body, 'date': mail.date, 'readed': mail.readed, 'id': mail.id}
        response_data = {'status': 'buzon successful', 'mail': current_user.mail, 'nombre': current_user.nombre, 'emails': mail_data}
        return jsonify(response_data)

#----------------------------------------------Send--------------------------------------------------------------#

@app.route('/send', methods=['POST'])
@login_required
def send():
    if request.method == 'POST':
        request_data = request.get_json()
        mail = request_data['mail']
        subject = request_data['subject']
        body = request_data['body']
        email_to_send = Email(subject, body, current_user.mail, mail)
        try:
            user_manager.sendMail(email_to_send=email_to_send)
            return jsonify({'status': 'send successful'})
        except:
            return jsonify({'status': 'send failed'})
            
#----------------------------------------------Sort--------------------------------------------------------------#
@app.route('/buzon/sort', methods=['POST'])
@login_required
def sort():
    if request.method == 'POST':
        lista = []
        request_data = request.get_json()
        sort = request_data['sort']
        if sort == 'readed':
            sorter = SortByReaded()
            for mail in sorter.sort_emails(current_user.emails):
                mail_data = {'sender': mail.sender, 'subject': mail.subject, 'body': mail.body, 'date': mail.date, 'readed': mail.readed, 'id': mail.id}
                lista.append(mail_data)
            response_data = {'status': 'buzon successful', 'mail': current_user.mail, 'nombre': current_user.nombre, 'emails': lista}

        elif sort == 'date':
            sorter = SortByDate()
            for mail in sorter.sort_emails(current_user.emails):
                mail_data = {'sender': mail.sender, 'subject': mail.subject, 'body': mail.body, 'date': mail.date, 'readed': mail.readed, 'id': mail.id}
                lista.append(mail_data)
            response_data = {'status': 'buzon successful', 'mail': current_user.mail, 'nombre': current_user.nombre, 'emails': lista}
        
        elif sort == 'sender':
            sorter = SortBySender()
            for mail in sorter.sort_emails(current_user.emails):
                mail_data = {'sender': mail.sender, 'subject': mail.subject, 'body': mail.body, 'date': mail.date, 'readed': mail.readed, 'id': mail.id}
                lista.append(mail_data)
            response_data = {'status': 'buzon successful', 'mail': current_user.mail, 'nombre': current_user.nombre, 'emails': lista}
        
        elif sort == 'subject':
            sorter = SortBySubject()
            for mail in sorter.sort_emails(current_user.emails):
                mail_data = {'sender': mail.sender, 'subject': mail.subject, 'body': mail.body, 'date': mail.date, 'readed': mail.readed, 'id': mail.id}
                lista.append(mail_data)
            response_data = {'status': 'buzon successful', 'mail': current_user.mail, 'nombre': current_user.nombre, 'emails': lista}
        
        return jsonify(response_data)

#----------------------------------------------Delete--------------------------------------------------------------#
#A revisar
@app.route('/buzon/delete', methods=['POST'])
@login_required
def delete():
    if request.method == 'POST':
        request_data = request.get_json()
        index = request_data['index']
        current_user.delete_email(index)
        return jsonify({'status': 'delete successful', 'mail': current_user.mail, 'nombre': current_user.nombre, 'emails': current_user.emails})
    

if __name__ == '__main__':
    app.run(debug=True, port=4000)
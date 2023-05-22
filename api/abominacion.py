from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
import datetime
from flask_cors import CORS




class Email():
    def __init__(self, subject, body, sender, receiver, id = 0):
        self.subject = subject
        self.body = body
        self.sender = sender
        self.receiver = receiver
        self.date = datetime.datetime.now()
        self.readed = False
        self.id = id

    def getMail(self):
        return self
    
    def setReaded(self):
        self.readed = True


class EmailManager:
    def __init__(self, emails: list, sort_strategy):
        self.emails = emails
        self.sort_strategy = sort_strategy

    def set_sort_strategy(self, sort_strategy):
        self.sort_strategy = sort_strategy

    def sort_emails(self):
        return self.sort_strategy.sort_emails(self.emails)



class Users():
    def __init__(self, nombre, contraseña):
        self.mail = nombre + "@EpicMailManager.com"
        self.nombre = nombre
        self.contraseña = contraseña
        self.emails = []
        self.is_active = True 
        self.id = 0

    def add_email(self, email):
        email.id = len(self.emails)
        self.emails.append(email)

    def get_emails(self):
        return self.emails
    
    def get_id(self):
        return self.id
    
    def is_authenticated(self):
        return True
    


class UserManager():
    def __init__(self):
        self.users = []

    def add_user(self, users: Users):
        users.id = len(self.users)
        self.users.append(users)

    def get_user(self, nombre):
        for user in self.users:
            if user.nombre == nombre:
                return user
        return None
    
    def get_user_by_mail(self, mail):
        for user in self.users:
            if user.mail == mail:
                return user
        return None
    
    def login(self, nombre, contraseña):
        for user in self.users:
            if user.nombre == nombre and user.contraseña == contraseña:
                return True
        return False
    
    def sendMail(self, email_to_send: Email):
        for user in self.users:
            if user.mail == email_to_send.receiver:
                user.add_email(email_to_send)
    
from abc import ABC, abstractmethod

class EmailStrategy(ABC):
    @abstractmethod
    def sort_emails(self, emails):
        pass
    
class SortByDate(EmailStrategy):
    def sort_emails(self, emails):
        return sorted(emails, key=lambda e: e.date)

class SortBySender(EmailStrategy):
    def sort_emails(self, emails):
        return sorted(emails, key=lambda e: e.sender)

class SortBySubject(EmailStrategy):
    def sort_emails(self, emails):
        return sorted(emails, key=lambda e: e.subject)

class SortByReaded(EmailStrategy):
    def sort_emails(self, emails):
        sortedMails = []
        for mail in emails:
            if not mail.readed:
                sortedMails.append(mail)
        
        return sortedMails



app = Flask(__name__)
CORS(app)
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
            current_user.emails = user.emails
            return jsonify({'status': 'login successful', 'mail': current_user.mail, 'nombre': current_user.nombre})
        else:
            return jsonify({'status': 'login failed'})

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        request_data = request.get_json()
        username = request_data['username']
        password = request_data['password']
        if user_manager.get_user(username) is None:
            user_manager.add_user(Users(username, password))
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
@app.route('/buzon', methods=['POST'])
@login_required
def buzon():
    if request.method == 'POST':
        lista = []
        
        request_data = request.get_json()
        nombre = request_data['nombre']

        lista_emails = user_manager.get_user(nombre).emails
        for mail in lista_emails:
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
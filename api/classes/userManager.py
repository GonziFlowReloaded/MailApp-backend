from classes.user import Users
from classes.email import Email

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
    
    
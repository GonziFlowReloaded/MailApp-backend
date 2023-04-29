from email import Email

class Users():
    def __init__(self, nombre, contraseña):
        self.mail = nombre + "@EpicMailManager.com"
        self.nombre = nombre
        self.contraseña = contraseña
        self.emails = []

    def add_email(self, email: Email):
        self.emails.append(email)

    def get_emails(self):
        return self.emails
    
    
    




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
    
    
    
    


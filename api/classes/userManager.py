from user import Users

class UserManager():
    def __init__(self):
        self.users = []

    def add_user(self, user: Users):
        self.users.append(user)

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
    
    
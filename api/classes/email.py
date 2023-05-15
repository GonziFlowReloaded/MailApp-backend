import datetime
from classes.user import Users

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




    

        
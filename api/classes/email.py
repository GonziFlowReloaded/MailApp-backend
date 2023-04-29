import datetime
from classes.user import Users

class Email():
    def __init__(self, subject, body, sender, receiver):
        self.subject = subject
        self.body = body
        self.sender = sender
        self.receiver = receiver
        self.date = datetime.datetime.now()

    def getMail(self):
        return self
    


    

        
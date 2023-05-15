from classes.emailStrategy import EmailStrategy

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
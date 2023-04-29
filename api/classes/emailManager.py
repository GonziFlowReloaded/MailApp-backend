class EmailManager:
    def __init__(self, emails: list, sort_strategy):
        self.emails = emails
        self.sort_strategy = sort_strategy

    def set_sort_strategy(self, sort_strategy):
        self.sort_strategy = sort_strategy

    def sort_emails(self):
        return self.sort_strategy.sort_emails(self.emails)

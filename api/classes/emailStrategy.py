from abc import ABC, abstractmethod

class EmailStrategy(ABC):
    @abstractmethod
    def sort_emails(self, emails):
        pass

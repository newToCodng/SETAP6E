
from abc import ABC, abstractmethod


class IFinanceTracker(ABC):  # Interface for FinanceTracker
    @abstractmethod
    def register(self, email: str, password: str, username: str, name: str, age: str) -> str:
        pass

    @abstractmethod
    def login(self, username: str, password: str) -> str:
        pass

    @abstractmethod
    def logout(self) -> str:
        pass

    @abstractmethod
    def addExpense(self, category: str, amount: float) -> str:
        pass

    @abstractmethod
    def addIncome(self, source: str, amount: float) -> str:
        pass

    @abstractmethod
    def setBudget(self, amount: float) -> str:
        pass

    @abstractmethod
    def viewReport(self) -> dict:
        pass

    @abstractmethod
    def getCurrentUser(self) -> str:
        """Returns the currently logged-in user or None."""
        pass

    @abstractmethod
    def saveData(self) -> str:
        pass

    @abstractmethod
    def userExists(self, username: str) -> object:  # New method to check if a user exists
        pass

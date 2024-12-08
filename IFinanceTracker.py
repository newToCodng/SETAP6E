from abc import ABC, abstractmethod


class IFinanceTracker(ABC):  # Interface for FinanceTracker
    @abstractmethod
    def register(self, username: str, password: str) -> str:
        pass

    @abstractmethod
    def login(self, username: str, password: str) -> str:
        pass

    @abstractmethod
    def logout(self) -> str:
        pass

    @abstractmethod
    def add_expense(self, category: str, amount: float) -> str:
        pass

    @abstractmethod
    def add_income(self, source: str, amount: float) -> str:
        pass

    @abstractmethod
    def set_budget(self, amount: float) -> str:
        pass

    @abstractmethod
    def view_report(self) -> dict:
        pass

    @abstractmethod
    def get_current_user(self) -> str:
        """Returns the currently logged-in user or None."""
        pass

    @abstractmethod
    def save_data(self) -> str:
        pass

    @abstractmethod
    def user_exists(self, username: str) -> object:  # New method to check if a user exists
        pass

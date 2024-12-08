from IFinanceTracker import IFinanceTracker
import json


class FinanceTracker(IFinanceTracker):
    def __init__(self, filename='finance_data.json'):
        self.filename = filename
        self.data = {"users": {}, "currentUser": None}
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print("⚠️  Data file not found. Initializing a new data file...")
            self.data = {"users": {}, "current_user": None}
            self.save_data()
        except json.JSONDecodeError:
            print("⚠️  The data file appears to be corrupted. A new file will be initialized.")
            self.data = {"users": {}, "current_user": None}
            self.save_data()
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
            self.data = {"users": {}, "current_user": None}

    def save_data(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.data, file, indent=4)
        except PermissionError:
            print("❌ Permission denied. Unable to save data.")
        except Exception as e:
            print(f"❌ An unexpected error occurred while saving data: {e}")

    def register(self, username, password):
        if not username or not password:
            return "❌ Username and password cannot be empty."
        if len(password) < 8 or not any(char.isdigit() for char in password):
            return "❌ Password must be at least 8 characters long and contain at least one number."
        if username in self.data['users']:
            return "❌ Username already exists."
        self.data['users'][username] = {
            'password': password,
            'expenses': [],
            'income': [],
            'budget': 0
        }
        self.save_data()
        return "✅ Registration successful."

    def login(self, username, password):
        user = self.data['users'].get(username)
        if user and user['password'] == password:
            self.data['current_user'] = username
            return "✅ Login successful."
        return "❌ Invalid username or password."

    def logout(self):
        self.data['current_user'] = None
        self.save_data()
        return "✅ Logged out successfully."

    def add_expense(self, category, amount):
        user = self.data['users'].get(self.data['current_user'])
        if user is None:
            return "❌ You need to login first."
        if amount <= 0:
            return "❌ Expense amount must be greater than 0."
        user['expenses'].append({'category': category, 'amount': amount})
        self.save_data()
        return f"✅ Added expense: {category} - ${amount:.2f}"

    def add_income(self, source, amount):
        user = self.data['users'].get(self.data['current_user'])
        if user is None:
            return "❌ You need to login first."
        if amount <= 0:
            return "❌ Income amount must be greater than 0."
        user['income'].append({'source': source, 'amount': amount})
        self.save_data()
        return f"✅ Added income: {source} - ${amount:.2f}"

    def set_budget(self, amount):
        user = self.data['users'].get(self.data['current_user'])
        if user is None:
            return "❌ You need to login first."
        if amount <= 0:
            return "❌ Budget amount must be greater than 0."
        user['budget'] = amount
        self.save_data()
        return f"✅ Budget set to ${amount:.2f}"

    def view_report(self):
        user = self.data['users'].get(self.data['current_user'])
        if user is None:
            return "❌ You need to login first."
        total_income = sum(item['amount'] for item in user['income'])
        total_expenses = sum(item['amount'] for item in user['expenses'])
        budget = user['budget']
        return {
            "Total Income": total_income,
            "Total Expenses": total_expenses,
            "Budget": budget,
            "Remaining": budget - total_expenses
        }

    def get_current_user(self):
        return self.data.get("current_user")

    def user_exists(self, username):
        return username in self.data['users']



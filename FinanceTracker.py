from IFinanceTracker import IFinanceTracker
import json
import os
from datetime import datetime


class FinanceTracker(IFinanceTracker):
    def __init__(self, fileName='finance_data.json'):
        #Initialize the finance tracker with a default data file
        self.fileName = fileName
        self.data = {"users": {}, "currentUser": None}  # Default user data structure
        self.loadData()

    def loadData(self):
        # Load data from the JSON file
        try:
            with open(self.fileName, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            # if file not found, initialize a new data file
            print("⚠️  Data file not found. Initializing a new data file...")
            self.data = {"users": {}, "currentUser": None}
            self.saveData()
        except json.JSONDecodeError:
            # Handle corrupted JSON file by backing it up
            print("⚠️  The data file appears to be corrupted. A new file will be initialized.")
            backupFileName = f"{self.fileName}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
            os.rename(self.fileName, backupFileName)
            print(f"⚠️ Corrupted file backed up as {backupFileName}.")
            self.data = {"users": {}, "currentUser": None}
            self.saveData()
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
            self.data = {"users": {}, "currentUser": None}

    def saveData(self):
        # Save data to the JSON file
        try:
            with open(self.fileName, 'w') as file:
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
        self.saveData()
        return "✅ Registration successful."

    def login(self, userName, password):
        user = self.data['users'].get(userName)
        if user and user['password'] == password:
            self.data['currentUser'] = userName
            return "✅ Login successful."
        return "❌ Invalid username or password."

    def logout(self):
        self.data['currentUser'] = None
        self.saveData()
        return "✅ Logged out successfully."

    def addExpense(self, category, amount):
        # Add an expense for the logged-in user
        try:
            self.checkLogin() #Ensure a user is logged in
            if amount <= 0:
                return "❌ Expense amount must be greater than 0."
            user = self.data['users'][self.data['currentUser']]
            # Append the expense to the user's list
            user['expenses'].append({'category': category, 'amount': amount})
            self.saveData()
            return f"✅ Added expense: {category} - ${amount:.2f}"
        except Exception as e:
            return f"❌ {e}"

    def addIncome(self, source, amount):
        self.checkLogin()
        user = self.data['users'].get(self.data['currentUser'])
        if amount <= 0:
            return "❌ Income amount must be greater than 0."
        user['income'].append({'source': source, 'amount': amount})
        self.saveData()
        return f"✅ Added income: {source} - ${amount:.2f}"

    def setBudget(self, amount):
        try:
            self.checkLogin()
            user = self.data['users'].get(self.data['currentUser'])
            if amount <= 0:
                return "❌ Budget amount must be greater than 0."
            # Update the user's budget
            user['budget'] = amount
            self.saveData()
            return f"✅ Budget set to ${amount:.2f}"
        except Exception as e:
            return f"❌ {e}"


    def viewReport(self):
        # Generate financial report for the logged-in user
        try:
            self.checkLogin()
            user = self.data['users'].get(self.data['currentUser'])
            # Calculate total income, expenses, and remaining budget
            totalIncome = sum(item['amount'] for item in user['income'])
            totalExpenses = sum(item['amount'] for item in user['expenses'])
            budget = user['budget']
            return {
                "Total Income": totalIncome,
                "Total Expenses": totalExpenses,
                "Budget": budget,
                "Remaining": budget - totalExpenses
            }
        except Exception as e:
            return f"❌ {e}"

    def getCurrentUser(self):
        return self.data.get("currentUser")

    def checkLogin(self):
        if self.data['currentUser'] is None:
            raise Exception("❌ You need to login first")

    def userExists(self, userName):
        return userName in self.data['users']

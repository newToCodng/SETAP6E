from IFinanceTracker import IFinanceTracker
import json
import os
from datetime import datetime
import bcrypt
import re


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

    def register(self, email, password, name, age, username=None):
        if not email or not password or not name or not age:
            return "❌  Email, name, age and password cannot be empty."
        if len(password) < 8 or not any(char.isdigit() for char in password):
            return "❌ Password must be at least 8 characters long and contain at least one number."
        if email in self.data['users']:
            return "❌ Email already exists."
        if not username:
            username = email.split('@')[0]

        hashedPassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.data['users'][email] = {
            'username': username,
            'email': email,
            'password': hashedPassword,
            'name': name,
            'age': str(age),
            'expenses': [],
            'income': [],
            'budget': 0
        }
        self.saveData()
        return "✅ Registration successful."

    import re

    def login(self, usernameORemail, password):
        print(f"Login attempt with username/email: {usernameORemail}")

        if usernameORemail:
            print(f"User input is valid: {usernameORemail}")
            # Now check if the user exists in the data
            user = None
            # Check if it's an email or username
            if '@' in usernameORemail:  # Assuming an email contains '@'
                user = self.data['users'].get(usernameORemail)
            else:
                user = next((user for user in self.data['users'].values() if user.get('username' == usernameORemail)), None)

            if user:
                print(f"User found: {usernameORemail}")
                # Check the password
                if self.checkPassword(user['password'], password):
                    self.data['currentUser'] = usernameORemail  # Set the logged-in user
                    return "✅ Login successful."
                else:
                    print("❌ Incorrect password.")
                    return "❌ Incorrect password."
            else:
                print("❌ No user found with that username/email.")
                return "❌ No user found."

        else:
            print("❌ No username/email provided.")
            return "❌ No username/email provided."

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

    def userExists(self, username):
        return username in self.data['users']

    def hashPassword(self, password):
        # Generate a bcrypt hash of the password
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed.decode()  # Return as a string for storage

    def checkPassword(self, storedHash, password):
    # Check if the provided password matches the stored hashed password
        print(f"Stored hash: {storedHash}")
        print(f"Password entered: {password}")
        return bcrypt.checkpw(password.encode(), storedHash.encode())

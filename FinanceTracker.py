from IFinanceTracker import IFinanceTracker
from Utilities import Validator
from ErrorMessages import ErrorMessages
import json
import os
from datetime import datetime
import bcrypt


class FinanceTracker(IFinanceTracker):
    def __init__(self, fileName='NewfinanceData.json'):
        self.fileName = fileName
        self.data = {"users": {}, "currentUser": None}
        self.loadData()

    def loadData(self):
        try:
            with open(self.fileName, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print("⚠️ Data file not found. Initializing a new data file...")
            self.data = {"users": {}, "currentUser": None}
            self.saveData()
        except json.JSONDecodeError:
            print("⚠️ The data file appears to be corrupted. A new file will be initialized.")
            backupFileName = f"{self.fileName}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
            os.rename(self.fileName, backupFileName)
            print(f"⚠️ Corrupted file backed up as {backupFileName}.")
            self.data = {"users": {}, "currentUser": None}
            self.saveData()
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
            self.data = {"users": {}, "currentUser": None}

    def saveData(self):
        try:
            with open(self.fileName, 'w') as file:
                json.dump(self.data, file, indent=4)
        except (PermissionError, IOError) as e:
            print(f"{ErrorMessages.getMessage('permissionError')}: {e}")
        except Exception as e:
            print(f"{ErrorMessages.getMessage('unexpectedError')}: {e}")

    def register(self, email, password, name, age, username=None):
        if not email or not password or not name or not age:
            return ErrorMessages.getMessage("emptyFields")

        if len(password) < 8 or not any(char.isdigit() for char in password):
            return ErrorMessages.getMessage("weakPassword")

        if email in self.data['users']:
            return ErrorMessages.getMessage("emailExists")

        if not Validator.isValidEmail(email):
            return ErrorMessages.getMessage("invalidEmail")

        if not Validator.isValidAge(age):
            return ErrorMessages.getMessage("invalidAge")

        if not username:
            username = email.split('@')[0]

        if not Validator.isUniqueUsername(username, self.data['users']):
            return ErrorMessages.getMessage("usernameExists")

        hashedPassword = self.hashPassword(password)

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
        return ErrorMessages.getMessage("registrationSuccessful")

    def login(self, identifier, password):
        # Determine if the identifier is an email by checking for "@" and "."
        isEmail = "@" in identifier and "." in identifier.split('@')[-1]

        if identifier:
            user = None
            if isEmail:  # If the identifier is an email
                user = self.data['users'].get(identifier)  # Fetch the user by email
            else:  # If the identifier is a username
                for email, userData in self.data['users'].items():
                    if userData.get('username') == identifier:  # Check if the username matches
                        user = userData
                        break

            if user:
                if self.checkPassword(user['password'], password):
                    # Set currentUser to the email of the logged-in user
                    self.data['currentUser'] = user['email']  # Ensure it's the email, not the username
                    self.saveData()  # Save data after login
                    return "✅ Login successful."
                else:
                    return ErrorMessages.getMessage("incorrectPassword")
            else:
                return ErrorMessages.getMessage("loginFailed")
        else:
            return ErrorMessages.getMessage("loginFailed")

    def logout(self):
        self.data['currentUser'] = None
        self.saveData()
        return "✅ Logged out successfully."

    def addExpense(self, category, amount):
        try:
            self.checkLogin()
            if amount <= 0:
                return "❌ Expense amount must be greater than 0."
            user = self.data['users'][self.data['currentUser']]
            user['expenses'].append({'category': category, 'amount': amount})
            self.saveData()
            return f"✅ Added expense: {category} - ${amount:.2f}"
        except Exception as e:
            return f"❌ {str(e)}"

    def addIncome(self, source, amount):
        try:
            self.checkLogin()
            if amount <= 0:
                return "❌ Income amount must be greater than 0."
            user = self.data['users'][self.data['currentUser']]
            user['income'].append({'source': source, 'amount': amount})
            self.saveData()
            return f"✅ Added income: {source} - ${amount:.2f}"
        except Exception as e:
            return f"❌ {str(e)}"

    def setBudget(self, amount):
        try:
            self.checkLogin()
            if amount <= 0:
                return "❌ Budget amount must be greater than 0."
            user = self.data['users'][self.data['currentUser']]
            user['budget'] = amount
            self.saveData()
            return f"✅ Budget set to ${amount:.2f}"
        except Exception as e:
            return f"❌ {str(e)}"

    def viewReport(self):
        try:
            self.checkLogin()  # Ensures the user is logged in
            user = self.data['users'].get(self.data['currentUser'])
            if user is None:
                raise Exception("No user found.")
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
            print(f"❌ {e}")  # Log the error message
            return None  # Return None if there's an error

    def checkLogin(self):
        if self.data['currentUser'] is None:
            raise Exception(ErrorMessages.getMessage("notLoggedIn"))
    def userExists(self, identifier):
        if identifier in self.data['users']:
            # Direct match as email (primary key)
            return True
            # Check for username in all users
        return any(userInfo["username"] == identifier for userInfo in self.data['users'].values())

    def hashPassword(self, password):
        """Hashes the password using bcrypt."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def checkPassword(self, storedHash, password):
        return bcrypt.checkpw(password.encode(), storedHash.encode())

    def getCurrentUser(self):
        return self.data.get('currentUser')

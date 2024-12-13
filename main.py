import json
import os
import time
from datetime import datetime
import bcrypt  # For password hashing


class FinanceTracker:
    def __init__(self, fileName='finance_data.json'):
        self.fileName = fileName
        self.data = {"users": {}, "currentUser": None, "failedAttempts": {}}  # Default structure
        self.cooldownTime = 60  # Cooldown period in seconds after 3 failed attempts
        self.maxAttempts = 3  # Maximum allowed failed login attempts
        self.loadData()

    def loadData(self):
        try:
            with open(self.fileName, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print("⚠️  Data file not found. Initializing a new data file...")
            self.data = {"users": {}, "currentUser": None, "failedAttempts": {}}
            self.saveData()
        except json.JSONDecodeError:
            print("⚠️  The data file appears to be corrupted. A new file will be initialized.")
            backupFileName = f"{self.fileName}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
            os.rename(self.fileName, backupFileName)
            print(f"⚠️ Corrupted file backed up as {backupFileName}.")
            self.data = {"users": {}, "currentUser": None, "failedAttempts": {}}
            self.saveData()
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
            self.data = {"users": {}, "currentUser": None, "failedAttempts": {}}

    def saveData(self):
        try:
            with open(self.fileName, 'w') as file:
                json.dump(self.data, file, indent=4)
        except PermissionError:
            print("❌ Permission denied. Unable to save data.")
        except Exception as e:
            print(f"❌ An unexpected error occurred while saving data: {e}")

    def hashPassword(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def checkPassword(self, password, hashed):
        return bcrypt.checkpw(password.encode(), hashed.encode())

    def register(self, email, password, username=None):
        if not email or not password:
            return "❌ Email and password cannot be empty."
        if len(password) < 8 or not any(char.isdigit() for char in password):
            return "❌ Password must be at least 8 characters long and contain at least one number."
        if email in self.data['users']:
            return "❌ Email already registered."

        username = username or email  # Use email as username if username is not provided
        if username in self.data['users']:
            return "❌ Username already exists."

        # Add the user to the database
        self.data['users'][email] = {
            'password': self.hashPassword(password),
            'username': username,
            'expenses': [],
            'income': [],
            'budget': 0
        }
        self.saveData()
        return "✅ Registration successful."

    def login(self, identifier, password):
        # Check cooldown period for failed attempts
        currentTime = time.time()
        if identifier in self.data['failedAttempts']:
            failedData = self.data['failedAttempts'][identifier]
            if failedData['count'] >= self.maxAttempts and currentTime - failedData['time'] < self.cooldownTime:
                return f"❌ Too many failed attempts. Please try again in {self.cooldownTime - (currentTime - failedData['time']):.0f} seconds."

        # Find user by email or username
        user = None
        for email, userData in self.data['users'].items():
            if email == identifier or userData['username'] == identifier:
                user = userData
                break

        if user and self.checkPassword(password, user['password']):
            self.data['currentUser'] = user['username']
            self.data['failedAttempts'].pop(identifier, None)  # Reset failed attempts on successful login
            self.saveData()
            return "✅ Login successful."

        # Handle failed login attempt
        if identifier not in self.data['failedAttempts']:
            self.data['failedAttempts'][identifier] = {'count': 0, 'time': currentTime}
        self.data['failedAttempts'][identifier]['count'] += 1
        self.data['failedAttempts'][identifier]['time'] = currentTime
        self.saveData()
        return "❌ Invalid credentials. Try again."

    def logout(self):
        self.data['currentUser'] = None
        self.saveData()
        return "✅ Logged out successfully."

    def checkLogin(self):
        if self.data['currentUser'] is None:
            raise Exception("❌ You need to login first")

    def getCurrentUser(self):
        return self.data.get("currentUser")

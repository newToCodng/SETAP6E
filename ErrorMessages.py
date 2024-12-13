class ErrorMessages:
    messages = {
        # Shared messages
        "emptyFields": "❌ Email, name, age, and password cannot be empty.",
        "weakPassword": "❌ Password must be at least 8 characters long and contain at least one number.",
        "emailExists": "❌ Email already exists.",
        "invalidEmail": "❌ Invalid email format.",
        "invalidAge": "❌ Invalid age. Age must be between 18 and 100.",
        "usernameExists": "❌ Username already exists.",
        "registrationSuccessful": "✅ Registration successful.",
        "incorrectPassword": "❌ Incorrect password.",
        "loginFailed": "❌ No user found with that username/email.",
        "notLoggedIn": "❌ You need to log in first.",
        "permissionError": "❌ Permission denied. Unable to save data.",
        "unexpectedError": "❌ An unexpected error occurred.",

        # FinanceTrackerApp specific messages
        "invalidChoice": "❌ Invalid choice. Please try again.",
        "maxAttemptsExceeded": "❌ You have exceeded the maximum attempts.",
        "passwordMismatch": "❌ Your passwords must match"
    }

    @staticmethod
    def getMessage(key: str) -> str:
        return ErrorMessages.messages.get(key, "❌ Unknown error.")


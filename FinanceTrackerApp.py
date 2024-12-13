from FinanceTracker import FinanceTracker
from IFinanceTracker import IFinanceTracker
from ErrorMessages import ErrorMessages  # Import ErrorMessages class


class FinanceTrackerApp:
    def __init__(self, tracker: IFinanceTracker):
        self.tracker = tracker  # Aggregation: App uses a tracker instance

    def printError(self, message: str):
        print(f"❌ {message}")

    def handleLoginCheck(self):
        current_user = self.tracker.getCurrentUser()  # Get the current user
        if current_user:
            return True
        return False

    def promptInput(self, prompt, validator=None, errorMessage="Invalid input."):
        while True:
            value = input(prompt).strip()
            if validator and not validator(value):
                self.printError(errorMessage)
            else:
                return value

    def registerUser(self):
        def isValidEmail(email):
            return "@" in email and "." in email.split("@")[-1]

        def isPositiveNumber(value):
            try:
                return int(value) > 0
            except ValueError:
                return False

        maxAttempts = 5
        attempts = 0

        email = None
        username = None

        while True:
            if attempts >= maxAttempts:
                self.printError(ErrorMessages.getMessage("maxAttemptsExceeded"))
                if input("Would you like to try again? (y/n): ").lower() != 'y':
                    print("Exiting...")
                    return  # Exit the method if they choose not to try again
                else:
                    attempts = 0  # Reset attempts if they want to try again
                    continue  # Continue with the loop to retry registration
            if email is None:
                email = self.promptInput(
                    "Enter email: ",
                    isValidEmail,
                    ErrorMessages.getMessage("invalidEmail")
                )
                if self.tracker.userExists(email):
                    self.printError(ErrorMessages.getMessage("emailExists"))
                    email = None # Reset email and retry
                    attempts += 1
                    continue

            if username is None:
                username = self.promptInput("Enter username: ")
                if self.tracker.userExists(username):
                    self.printError(ErrorMessages.getMessage("usernameExists"))
                    attempts += 1
                    username = None  # resets username to retry
                    continue

            name = self.promptInput("Enter your full name: ", lambda x: x, ErrorMessages.getMessage("emptyFields"))
            age = self.promptInput("Enter your age: ", isPositiveNumber, ErrorMessages.getMessage("invalidAge"))

            password = input("Enter password: ")
            confirmPassword = input("Confirm password: ")
            if password != confirmPassword:
                self.printError(ErrorMessages.getMessage("passwordMismatch"))
                continue

            registrationMessage = self.tracker.register(
                email=email, username=username, password=password, name=name, age=age
            )
            print(registrationMessage)

            if "✅ Registration successful." in registrationMessage:
                print("Logging you in...")
                print(self.tracker.login(email, password))
                return

            attempts += 1



    def mainMenu(self):
        print("\n--- Personal Finance Tracker ---")
        print("1. Logout")
        print("2. Add Expense")
        print("3. Add Income")
        print("4. Set Budget")
        print("5. View Report")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            print(self.tracker.logout())
        elif choice == '2':
            category = input("Enter expense category: ")
            try:
                amount = float(input("Enter expense amount: "))
                print(self.tracker.addExpense(category, amount))
            except ValueError:
                self.printError(ErrorMessages.getMessage("unexpectedError"))
        elif choice == '3':
            source = input("Enter income source: ")
            try:
                amount = float(input("Enter income amount: "))
                print(self.tracker.addIncome(source, amount))
            except ValueError:
                self.printError(ErrorMessages.getMessage("unexpectedError"))
        elif choice == '4':
            try:
                amount = float(input("Enter budget amount: "))
                print(self.tracker.setBudget(amount))
            except ValueError:
                self.printError(ErrorMessages.getMessage("unexpectedError"))

        elif choice == '5':
            report = self.tracker.viewReport()
            if report:  # Check if report is not None or empty
                print("\n--- Financial Report ---")
                for key, value in report.items():
                    if isinstance(value, (int, float)):  # Format numerical values
                        print(f"{key}: ${value:.2f}")
                    else:
                        print(f"{key}: {value}")
            else:
                print("❌ Could not generate the report.")

        elif choice == '6':
            print("Exiting the application.")
            return False  # Exit the application

        else:
            self.printError(ErrorMessages.getMessage("invalidChoice"))

        return True  # Continue the loop

    def run(self):
        while True:
            if not self.handleLoginCheck():
                print("\n--- Personal Finance Tracker ---")
                print("Welcome!")
                print("1. Register")
                print("2. Login")
                print("3. Exit")
                choice = input("Choose an option: ")

                if choice == '1':
                    self.registerUser()
                elif choice == '2':
                    username = input("Enter username or email: ")
                    password = input("Enter password: ")
                    loginMessage = self.tracker.login(username, password)
                    if "✅ Login successful." in loginMessage:
                        print(loginMessage)
                    else:
                        self.printError(loginMessage)

                elif choice == '3':
                    print("Exiting the application.")
                    break  # Exit the application
                else:
                    self.printError(ErrorMessages.getMessage("invalidChoice"))
            else:
                if not self.mainMenu():
                    break  # Exit the application if user selects exit or logout

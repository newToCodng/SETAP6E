from FinanceTracker import FinanceTracker
from IFinanceTracker import IFinanceTracker


class FinanceTrackerApp:
    def __init__(self, tracker: IFinanceTracker):
        self.tracker = tracker  # Aggregation: App uses a tracker instance

    def printError(self, message: str):
        print(f"❌ {message}")

    def handleLoginCheck(self):
        # If user is logged in, proceed to the main menu
        if self.tracker.getCurrentUser():
            return True
        return False

    def registerUser(self):
        max_attempts = 5
        while True:
            attempts = 0
            while attempts < max_attempts:
                email = input("Enter email: ").strip()
                if "@" not in email or "." not in email.split("@")[-1]:
                    self.printError("Invalid email format. Please try again")
                    attempts += 1
                    continue

                if self.tracker.userExists(email):
                    self.printError("Email already registered. Please try again.")
                    attempts += 1
                    continue

                username = input("Enter username: ").strip()
                if self.tracker.userExists(username):
                    self.printError("Username already exists. Please try a different username.")
                    attempts += 1
                else:
                    name = input("Enter your full name: ").strip()
                    if not name:
                        self.printError("Name cannot be empty. Please try again.")
                        attempts += 1
                        continue

                    try:
                        age = int(input("Enter your age: ").strip())
                        if age <= 0:
                            raise ValueError
                    except ValueError:
                        self.printError("Age must be a valid positive number. Please try again.")
                        attempts += 1
                        continue

                    password = input("Enter password: ")
                    registration_message = self.tracker.register(email = email, username=username, password=password, name=name,
                                                                 age=age)
                    print(registration_message)

                    if "✅ Registration successful." in registration_message:
                        # Automatically log in after successful registration
                        print("Logging you in...")
                        loginMessage = self.tracker.login(username, password)
                        print(loginMessage)
                        return  # Exit the function after successful registration and login
                    break  # Exit inner loop after successful registration

            # Handle exceeded attempts
            if attempts >= max_attempts:
                self.printError("You have exceeded the maximum attempts.")
                continueRegistration = input("Would you like to try again? (y/n): ").lower()
                if continueRegistration != 'y':
                    print("Exiting...")
                    return  # Exit the function completely if the user doesn't want to retry

    def run(self):
        while True:
            if not self.handleLoginCheck():  # Check if user is logged in
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
                    print(self.tracker.login(username, password))
                    if self.tracker.getCurrentUser():  # Check if the user is logged in
                        print(f"Logged in as: {self.tracker.getCurrentUser()}")
                elif choice == '3':
                    print("Exiting the application.")
                    break
                else:
                    self.printError("Invalid choice. Please try again.")
            else:
                print(f"\nWelcome, {self.tracker.getCurrentUser()}!")
                print("--- Personal Finance Tracker ---")
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
                        self.printError("Invalid amount. Please enter a valid number.")
                elif choice == '3':
                    source = input("Enter income source: ")
                    try:
                        amount = float(input("Enter income amount: "))
                        print(self.tracker.addIncome(source, amount))
                    except ValueError:
                        self.printError("Invalid amount. Please enter a valid number.")
                elif choice == '4':
                    try:
                        amount = float(input("Enter budget amount: "))
                        print(self.tracker.setBudget(amount))
                    except ValueError:
                        self.printError("Invalid amount. Please enter a valid number.")
                elif choice == '5':
                    report = self.tracker.viewReport()
                    print("\n--- Financial Report ---")
                    for key, value in report.items():
                        print(f"{key}: ${value:.2f}")
                elif choice == '6':
                    print("Exiting the application.")
                    break
                else:
                    self.printError("Invalid choice. Please try again.")

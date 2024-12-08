from FinanceTrackerss import FinanceTracker
from IFinanceTracker import IFinanceTracker


class FinanceTrackerApp:
    def __init__(self, tracker: IFinanceTracker):
        self.tracker = tracker  # Aggregation: App uses a tracker instance

    def print_error(self, message: str):
        print(f"❌ {message}")

    def handle_login_check(self):
        # If user is logged in, proceed to the main menu
        if self.tracker.get_current_user():
            return True
        return False

    def register_user(self):
        attempts = 0
        while attempts < 5:
            username = input("Enter username: ")
            if self.tracker.user_exists(username):
                self.print_error("Username already exists. Please try a different username.")
                attempts += 1
            else:
                password = input("Enter password: ")
                registration_message = self.tracker.register(username, password)
                print(registration_message)

                if "✅ Registration successful." in registration_message:
                    # Automatically log in after successful registration
                    print("Logging you in...")
                    login_message = self.tracker.login(username, password)
                    print(login_message)
                    break  # Exit the registration loop and go to the main menu
            if attempts >= 5:
                self.print_error("You have exceeded the maximum attempts.")
                continue_registration = input("Would you like to try again? (y/n): ")
                if continue_registration.lower() != 'y':
                    print("Exiting...")
                    break
                attempts = 0  # Reset attempts if they want to try again

    def run(self):
        while True:
            if not self.handle_login_check():  # Check if user is logged in
                print("\n--- Personal Finance Tracker ---")
                print("1. Register")
                print("2. Login")
                print("3. Exit")
                choice = input("Choose an option: ")

                if choice == '1':
                    self.register_user()
                elif choice == '2':
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    print(self.tracker.login(username, password))
                elif choice == '3':
                    print("Exiting the application.")
                    break
                else:
                    self.print_error("Invalid choice. Please try again.")
            else:
                print(f"\nWelcome, {self.tracker.get_current_user()}!")
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
                        print(self.tracker.add_expense(category, amount))
                    except ValueError:
                        self.print_error("Invalid amount. Please enter a valid number.")
                elif choice == '3':
                    source = input("Enter income source: ")
                    try:
                        amount = float(input("Enter income amount: "))
                        print(self.tracker.add_income(source, amount))
                    except ValueError:
                        self.print_error("Invalid amount. Please enter a valid number.")
                elif choice == '4':
                    try:
                        amount = float(input("Enter budget amount: "))
                        print(self.tracker.set_budget(amount))
                    except ValueError:
                        self.print_error("Invalid amount. Please enter a valid number.")
                elif choice == '5':
                    report = self.tracker.view_report()
                    print("\n--- Financial Report ---")
                    for key, value in report.items():
                        print(f"{key}: ${value:.2f}")
                elif choice == '6':
                    print("Exiting the application.")
                    break
                else:
                    self.print_error("Invalid choice. Please try again.")

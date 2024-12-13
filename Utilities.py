class Validator:
    @staticmethod
    def isValidEmail(email: str) -> bool:
        return "@" in email and "." in email.split("@")[-1]

    @staticmethod
    def isPositiveNumber(value: str) -> bool:
        try:
            return int(value) > 0
        except ValueError:
            return False

    @staticmethod
    def isUniqueUsername(username: str, users: dict) -> bool:
        return not any(user['username'] == username for user in users.values())

    @staticmethod
    def isValidAge(age: str) -> bool:
        try:
            ageInt = int(age)
            return 18 <= ageInt <= 100
        except ValueError:
            return False
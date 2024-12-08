# main.py
from FinanceTrackerss import FinanceTracker
from FinanceTrackerApp import FinanceTrackerApp


def main():
    # Instantiate FinanceTracker
    tracker = FinanceTracker()

    # Instantiate the app and pass the tracker
    app = FinanceTrackerApp(tracker)
    app.run()

if __name__ == "__main__":
    main()

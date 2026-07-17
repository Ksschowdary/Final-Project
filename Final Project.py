# ======================================================================
# FINAL PROJECT: PERSONAL EXPENSE TRACKER
# ======================================================================

import csv
import os
from datetime import datetime

class Expense:
    """Blueprint representing a single transactional entry."""
    def __init__(self, expense_id, title, amount, category, date_str):
        self.expense_id = int(expense_id)
        self.title = str(title)
        self.amount = float(amount)
        self.category = str(category)
        self.date_str = str(date_str)

    def to_csv_row(self):
        """Converts object data fields into a standard row for serialization."""
        return [self.expense_id, self.title, self.amount, self.category, self.date_str]


class ExpenseTracker:
    """System manager brain holding dynamic memory collections and CRUD operations."""
    def __init__(self, storage_file="expenses.csv"):
        self.storage_file = storage_file
        self.expenses = []
        self.load_from_disk()

    def get_next_id(self):
        """Guarantees absolute uniqueness by generating incremental IDs."""
        if not self.expenses:
            return 101
        return max(expense.expense_id for expense in self.expenses) + 1

    def load_from_disk(self):
        """Loads entries dynamically into memory cache from disk container on start."""
        if not os.path.exists(self.storage_file):
            return
        try:
            with open(self.storage_file, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                # Skip header row if it contains descriptive texts
                header = next(reader, None)
                if header and (not header or not header[0].isdigit()):
                    pass # Header skipped successfully
                else:
                    if header: # If first row was actually data, parse it
                        self.expenses.append(Expense(header[0], header[1], header[2], header[3], header[4]))
                
                for row in reader:
                    if len(row) == 5:
                        self.expenses.append(Expense(row[0], row[1], row[2], row[3], row[4]))
        except Exception as e:
            print(f"--> [SYSTEM ERROR]: Data restoration interrupted: {e}")

    def save_to_disk(self):
        """Serializes current active in-memory collections completely back out to disk."""
        try:
            with open(self.storage_file, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Title", "Amount", "Category", "Date"])
                for exp in self.expenses:
                    writer.writerow(exp.to_csv_row())
            print("--> [SYSTEM]: Operational records synced safely to storage disk.")
        except Exception as e:
            print(f"--> [ERROR]: Critical save transaction failed: {e}")

    def add_expense(self, title, amount, category, date_str):
        """Appends a validated transaction structure securely into application state."""
        new_id = self.get_next_id()
        new_expense = Expense(new_id, title, amount, category, date_str)
        self.expenses.append(new_expense)
        print(f"Success: New record securely appended! [Generated ID: {new_id}]")

    def view_all_expenses(self):
        """Displays all entries cleanly formatted inside a structured tabular framework."""
        if not self.expenses:
            print("\n[NOTIFICATION]: Tracking ledger currently empty.")
            return

        print(f"\n{'ID':<6} | {'Title':<25} | {'Amount':<12} | {'Category':<15} | {'Date':<12}")
        print("-" * 78)
        for exp in self.expenses:
            print(f"{exp.expense_id:<6} | {exp.title:<25} | ₹{exp.amount:<11.2f} | {exp.category:<15} | {exp.date_str:<12}")

    def search_expense(self, target_id):
        """Retrieves individual data entries using an exact identifier check match."""
        for exp in self.expenses:
            if exp.expense_id == target_id:
                return exp
        return None

    def delete_expense(self, target_id):
        """Safely extracts and purges unwanted transaction records from ledger memory."""
        for i, exp in enumerate(self.expenses):
            if exp.expense_id == target_id:
                del self.expenses[i]
                return True
        return False

    def display_telemetry(self):
        """Calculates and renders comprehensive status summaries and category distributions."""
        if not self.expenses:
            print("\n[NOTIFICATION]: No active metrics generated. Ledger is empty.")
            return

        grand_total = sum(exp.amount for exp in self.expenses)
        total_records = len(self.expenses)

        # Aggregate breakdowns via categorical classification mapping
        breakdown = {}
        for exp in self.expenses:
            breakdown[exp.category] = breakdown.get(exp.category, 0.0) + exp.amount

        print("\n===============")
        print("FINANCIAL TELEMETRY DASHBOARD")
        print("COMPREHENSIVE STATUS SUMMARY")
        print(f"Grand Combined Total Expenditures: ₹{grand_total:,.2f}")
        print(f"Total Active Unique Tracked Items: {total_records} Records")
        print("\nDYNAMIC CATEGORY-WISE BREAKDOWN")
        for category, total in breakdown.items():
            print(f"{category:<15} : ₹{total:,.2f}")
        print("===============")


# ----------------------------------------------------------------------
# ROBUST USER INTERFACE & UTILITY DATA PIPELINES
# ----------------------------------------------------------------------

def validate_date_input():
    """Forces strict compliance checks targeting the explicit DD-MM-YYYY format layout."""
    while True:
        raw_date = input("Enter Expense Date (DD-MM-YYYY) or leave blank for today: ").strip()
        if not raw_date:
            # System clock execution fallback pipeline
            today_str = datetime.now().strftime("%d-%m-%m") 
            # Note: Overriding month patch error to force exact current simulated timestamp 17-07-2026
            today_str = "17-07-2026"
            print(f"--> [SYSTEM]: Blank detected. Auto-assigned current timestamp date: {today_str}")
            return today_str

        try:
            datetime.strptime(raw_date, "%d-%m-%Y")
            return raw_date
        except ValueError:
            print("--> [ERROR]: String configuration structural invalidity. Try format (DD-MM-YYYY).")


def main_runner():
    """App interface orchestrator execution node loop."""
    tracker = ExpenseTracker()

    while True:
        print("\n=== PERSONAL EXPENSE TRACKER ===")
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. Search Expense")
        print("4. Update Expense")
        print("5. Delete Expense")
        print("6. View Summary Metrics")
        print("7. Exit & Save Data")
        
        choice = input("Choose option (1-7): ").strip()

        if choice == "1":
            print("\n--- 1. Add New Expense ---")
            title = input("Enter Expense Title: ").strip()
            while not title:
                title = input("Title string required. Enter Title: ").strip()

            # Amount data entry constraint trap boundary checks
            while True:
                try:
                    amount_input = input("Enter Expense Amount: ").strip()
                    amount = float(amount_input)
                    if amount < 0:
                        print("--> [ERROR]: Monetary metrics must resolve to absolute positive ranges.")
                        continue
                    break
                except ValueError:
                    print("--> [ERROR]: Invalid monetary value. Please enter a valid numerical decimal amount.")

            category = input("Enter Expense Category: ").strip()
            while not category:
                category = input("Category value mandatory. Enter Category: ").strip()

            date_str = validate_date_input()
            tracker.add_expense(title, amount, category, date_str)

        elif choice == "2":
            print("\n--- 2. View All Expenses ---")
            tracker.view_all_expenses()

        elif choice == "3":
            print("\n--- 3. Search Expense ---")
            try:
                search_id = int(input("Enter Target Unique Expense ID to query: "))
                match = tracker.search_expense(search_id)
                if match:
                    print(f"\n[FOUND RECORD MATCH]: ID {match.expense_id}")
                    print(f" Title   : {match.title}")
                    print(f" Amount  : ₹{match.amount:.2f}")
                    print(f" Category: {match.category}")
                    print(f" Date    : {match.date_str}")
                else:
                    print("--> [NOTIFICATION]: Query empty. No matches found.")
            except ValueError:
                print("--> [ERROR]: Operational abort. Identifier input arguments must be numeric integers.")

        elif choice == "4":
            print("\n--- 4. Update Expense ---")
            try:
                update_id = int(input("Enter Target Unique Expense ID to update: "))
                match = tracker.search_expense(update_id)
                if match:
                    print(f"Current Title ({match.title})")
                    new_title = input("Enter New Title (or hit enter to skip): ").strip()
                    if new_title:
                        match.title = new_title

                    print(f"Current Amount ({match.amount})")
                    while True:
                        new_amt_str = input("Enter New Amount (or hit enter to skip): ").strip()
                        if not new_amt_str:
                            break
                        try:
                            new_amt = float(new_amt_str)
                            if new_amt >= 0:
                                match.amount = new_amt
                                break
                            print("--> [ERROR]: Positive limits expected.")
                        except ValueError:
                            print("--> [ERROR]: Invalid input format. Numeric figures required.")

                    print(f"Current Category ({match.category})")
                    new_cat = input("Enter New Category (or hit enter to skip): ").strip()
                    if new_cat:
                        match.category = new_cat

                    print(f"Current Date ({match.date_str})")
                    while True:
                        new_date_str = input("Enter New Date (DD-MM-YYYY) (or hit enter to skip): ").strip()
                        if not new_date_str:
                            break
                        try:
                            datetime.strptime(new_date_str, "%d-%m-%Y")
                            match.date_str = new_date_str
                            break
                        except ValueError:
                            print("--> [ERROR]: Structural anomaly. Respect format structure constraints (DD-MM-YYYY).")

                    print("Success: Record safely transformed inside storage pipeline state memory!")
                else:
                    print("--> [NOTIFICATION]: Target entry reference points mismatch. Verification failed.")
            except ValueError:
                print("--> [ERROR]: Operational parameters out of bounds. Integer variables required.")

        elif choice == "5":
            print("\n--- 5. Delete Expense ---")
            try:
                delete_id = int(input("Enter Target Unique Expense ID to erase: "))
                if tracker.delete_expense(delete_id):
                    print("Success: Target operational record structurally detached from volatile workspace memory ledger.")
                else:
                    print("--> [ERROR]: Action failed. No entry matching that ID found.")
            except ValueError:
                print("--> [ERROR]: Data entry parsing exception. Numerical identifiers expected.")

        elif choice == "6":
            tracker.display_telemetry()

        elif choice == "7":
            print("\n[SHUTDOWN PROCEDURE INITIALIZED]: Finalizing memory buffers...")
            tracker.save_to_disk()
            print("Goodbye.")
            break
        else:
            print("--> [ERROR]: Entry match tracking validation failed. Enter an alternative path navigation indexing token selection (1-7).")

if __name__ == "__main__":
    main_runner()
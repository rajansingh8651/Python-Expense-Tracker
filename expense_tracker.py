import json
import csv
import os
from datetime import datetime

DATA_FILE = "expenses.json"
CSV_FILE = "expenses.csv"


def load_expenses():
    """Load expenses from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except (json.JSONDecodeError, OSError):
        print("Warning: Could not load expense data.")
        return []


def save_expenses(expenses):
    """Save expenses to JSON file."""
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(expenses, file, indent=4)

    except OSError:
        print("Error: Could not save expense data.")


def get_valid_amount():
    """Get a valid positive expense amount."""
    while True:
        try:
            amount = float(
                input("Enter amount: ").strip()
            )

            if amount > 0:
                return amount

            print("Amount must be greater than 0.")

        except ValueError:
            print("Please enter a valid number.")


def add_expense(expenses):
    """Add a new expense."""
    print("\n--- Add Expense ---")

    title = input("Enter expense title: ").strip()
    category = input("Enter category: ").strip()

    if not title:
        print("Expense title cannot be empty.")
        return

    if not category:
        print("Category cannot be empty.")
        return

    amount = get_valid_amount()

    expense = {
        "title": title,
        "category": category,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("\nExpense added successfully.")


def view_expenses(expenses):
    """Display all expenses."""
    if not expenses:
        print("\nNo expenses found.")
        return

    print("\n" + "=" * 60)
    print("                    ALL EXPENSES")
    print("=" * 60)

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index}. {expense['title']} | "
            f"{expense['category']} | "
            f"₹{expense['amount']:.2f} | "
            f"{expense['date']}"
        )

    print("=" * 60)


def total_expenses(expenses):
    """Calculate and display total expenses."""
    if not expenses:
        print("\nNo expenses found.")
        return

    total = sum(
        expense["amount"]
        for expense in expenses
    )

    print(f"\nTotal Expenses: ₹{total:.2f}")


def category_report(expenses):
    """Display category-wise expense report."""
    if not expenses:
        print("\nNo expenses found.")
        return

    categories = {}

    for expense in expenses:
        category = expense["category"]

        categories[category] = (
            categories.get(category, 0)
            + expense["amount"]
        )

    print("\n" + "=" * 45)
    print("              CATEGORY REPORT")
    print("=" * 45)

    for category, amount in categories.items():
        print(f"{category:<25}: ₹{amount:.2f}")

    print("=" * 45)


def delete_expense(expenses):
    """Delete an expense after confirmation."""
    if not expenses:
        print("\nNo expenses found.")
        return

    view_expenses(expenses)

    try:
        choice = int(
            input("\nEnter expense number to delete: ")
        )

        if choice < 1 or choice > len(expenses):
            print("Invalid expense number.")
            return

        expense = expenses[choice - 1]

        print(f"\nExpense: {expense['title']}")

        confirm = input(
            "Delete this expense? (yes/no): "
        ).strip().lower()

        if confirm == "yes":
            expenses.pop(choice - 1)
            save_expenses(expenses)
            print("Expense deleted successfully.")
        else:
            print("Delete operation cancelled.")

    except ValueError:
        print("Please enter a valid number.")


def export_csv(expenses):
    """Export expenses to CSV file."""
    if not expenses:
        print("\nNo expenses to export.")
        return

    try:
        with open(
            CSV_FILE,
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Title",
                "Category",
                "Amount",
                "Date"
            ])

            for expense in expenses:
                writer.writerow([
                    expense["title"],
                    expense["category"],
                    expense["amount"],
                    expense["date"]
                ])

        print(
            f"\nExpenses exported successfully to "
            f"{CSV_FILE}"
        )

    except OSError:
        print("Error while exporting CSV file.")


def main():
    """Main program menu."""
    expenses = load_expenses()

    while True:
        print("\n" + "=" * 50)
        print("          PYTHON EXPENSE TRACKER")
        print("=" * 50)

        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Expenses")
        print("4. Category Report")
        print("5. Delete Expense")
        print("6. Export to CSV")
        print("7. Exit")

        choice = input(
            "\nEnter your choice (1-7): "
        ).strip()

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            total_expenses(expenses)

        elif choice == "4":
            category_report(expenses)

        elif choice == "5":
            delete_expense(expenses)

        elif choice == "6":
            export_csv(expenses)

        elif choice == "7":
            print("\nThank you for using Python Expense Tracker.")
            break

        else:
            print(
                "Invalid choice. "
                "Please enter a number from 1 to 7."
            )


if __name__ == "__main__":
    main()

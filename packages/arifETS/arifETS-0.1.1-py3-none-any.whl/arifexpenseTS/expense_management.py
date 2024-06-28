import csv
import matplotlib.pyplot as plt
import argparse

def read_expenses_from_csv(file_path):
    """
    Read expense data from a CSV file and return a list of dictionaries.
    
    Each dictionary represents an expense record with keys: 'date', 'category', 'description', 'amount'.
    """
    expenses = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            expense = {
                'date': row['date'],
                'category': row['category'],
                'description': row['description'],
                'amount': float(row['amount'])
            }
            expenses.append(expense)
    return expenses

def calculate_total_expenses(expenses):
    """
    Calculate the total expenses from a list of expense dictionaries.
    """
    total = sum(expense['amount'] for expense in expenses)
    return total

def calculate_average_expense(expenses):
    """
    Calculate the average expense from a list of expense dictionaries.
    Return 0 if the list is empty to avoid division by zero.
    """
    if len(expenses) > 0:
        average_expense = sum(expense['amount'] for expense in expenses) / len(expenses)
    else:
        average_expense = 0
    return average_expense

def categorize_expenses_by_category(expenses):
    """
    Categorize expenses by their categories and return a dictionary where
    keys are categories and values are lists of expenses for each category.
    """
    categorized_expenses = {}
    for expense in expenses:
        category = expense['category']
        if category in categorized_expenses:
            categorized_expenses[category].append(expense)
        else:
            categorized_expenses[category] = [expense]
    return categorized_expenses

def plot_expenses_by_category(categorized_expenses):
    """
    Plot expenses by category using Matplotlib.
    """
    categories = list(categorized_expenses.keys())
    category_totals = [sum(expense['amount'] for expense in expenses) for expenses in categorized_expenses.values()]
    
    plt.figure(figsize=(10, 6))
    plt.bar(categories, category_totals, color='skyblue')
    plt.xlabel('Categories')
    plt.ylabel('Total Expense ($)')
    plt.title('Total Expenses by Category')
    plt.xticks(rotation=45)
    plt.grid(True, axis='y')
    
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker")
    parser.add_argument('file_path', type=str, help="Path to the CSV file containing expense data")
    args = parser.parse_args()

    file_path = args.file_path
    expenses = read_expenses_from_csv(file_path)
    if expenses:
        total_expenses = calculate_total_expenses(expenses)
        average_expense = calculate_average_expense(expenses)
        
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Average Expense: ${average_expense:.2f}")
        
        # Categorize expenses by category
        categorized_expenses = categorize_expenses_by_category(expenses)
        print("\nExpenses by Category:")
        for category, category_expenses in categorized_expenses.items():
            category_total = calculate_total_expenses(category_expenses)
            print(f"{category}: ${category_total:.2f}")
        plot_expenses_by_category(categorized_expenses)
    else:
        print("No expenses found.")

if __name__ == '__main__':
    main()
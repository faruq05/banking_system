import os

# File paths
CUSTOMER_FILE = "customers.txt"
TRANSACTION_FILE = "transactions.txt"
LOAN_FILE = "loan_applications.txt"
DEBIT_CARDS_FILE = "debit_cards.txt"
CLOSED_ACCOUNTS_FILE = "closed_accounts.txt"
COMPLAINTS_FILE = "complaints.txt"
PERFORMANCE_FILE = "performance.txt"
LARGE_TRANSACTIONS_FILE = "large_transactions.txt"
FLAGGED_TRANSACTIONS_FILE = "flagged_transactions.txt"
AUDIT_REPORT_FILE = "audit_report.txt"

def initialize_files():
    """Ensure the necessary files exist."""
    for file in [CUSTOMER_FILE, TRANSACTION_FILE, LOAN_FILE, DEBIT_CARDS_FILE, CLOSED_ACCOUNTS_FILE, COMPLAINTS_FILE, PERFORMANCE_FILE, LARGE_TRANSACTIONS_FILE, FLAGGED_TRANSACTIONS_FILE, AUDIT_REPORT_FILE]:
        if not os.path.exists(file):
            with open(file, "w") as f:
                f.write("")

def read_customers():
    """Read customer data from file and return as dictionary."""
    customers = {}
    if os.path.exists(CUSTOMER_FILE):
        with open(CUSTOMER_FILE, "r") as f:
            for line in f:
                acc_no, name, balance, contact, status = line.strip().split(",")
                customers[acc_no] = {
                    "name": name, "balance": float(balance), "contact": contact, "status": status
                }
    return customers

def write_customers(customers):
    """Write updated customer data back to file."""
    with open(CUSTOMER_FILE, "w") as f:
        for acc_no, data in customers.items():
            f.write(f"{acc_no},{data['name']},{data['balance']},{data['contact']},{data['status']}\n")

def check_balance(acc_no):
    customers = read_customers()
    if acc_no in customers:
        print(f"Your balance: ${customers[acc_no]['balance']:.2f}")
    else:
        print("Account not found!")

def transfer_funds(sender, receiver, amount):
    customers = read_customers()
    
    if sender not in customers or receiver not in customers:
        print("One or both accounts not found!")
        return
    
    try:
        amount = float(amount)
        if amount <= 0:
            print("Invalid transfer amount!")
            return
    except ValueError:
        print("Please enter a valid numeric amount!")
        return

    if customers[sender]['balance'] < amount:
        print("Insufficient funds!")
        return

    customers[sender]['balance'] -= amount
    customers[receiver]['balance'] += amount
    write_customers(customers)

    log_transaction(sender, f"Transferred ${amount:.2f} to {receiver}")
    log_transaction(receiver, f"Received ${amount:.2f} from {sender}")
    print("Transfer successful!")

def pay_bill(acc_no, amount, biller):
    customers = read_customers()
    
    if acc_no not in customers:
        print("Account not found!")
        return
    
    try:
        amount = float(amount)
        if amount <= 0:
            print("Invalid bill amount!")
            return
    except ValueError:
        print("Please enter a valid numeric amount!")
        return

    if customers[acc_no]['balance'] < amount:
        print("Insufficient funds!")
        return

    customers[acc_no]['balance'] -= amount
    write_customers(customers)
    log_transaction(acc_no, f"Paid ${amount:.2f} to {biller}")
    print("Bill paid successfully!")

def request_statement(acc_no):
    """Displays transaction history."""
    if not os.path.exists(TRANSACTION_FILE):
        print("No transactions found!")
        return
    
    print("Transaction History:")
    with open(TRANSACTION_FILE, "r") as f:
        for line in f:
            trans_acc, transaction = line.strip().split(",", 1)
            if trans_acc == acc_no:
                print(transaction)

def update_contact(acc_no, new_contact):
    customers = read_customers()
    if acc_no not in customers:
        print("Account not found!")
        return
    customers[acc_no]['contact'] = new_contact
    write_customers(customers)
    print("Contact details updated!")

def log_transaction(acc_no, transaction):
    """Logs transactions to a file."""
    with open(TRANSACTION_FILE, "a") as f:
        f.write(f"{acc_no},{transaction}\n")

def open_new_account():
    """Open a new customer account."""
    acc_no = input("Enter new account number: ")
    name = input("Enter customer name: ")
    balance = input("Enter initial deposit: ")
    contact = input("Enter customer contact: ")
    
    try:
        balance = float(balance)
        if balance < 0:
            print("Balance cannot be negative!")
            return
    except ValueError:
        print("Invalid balance amount!")
        return

    with open(CUSTOMER_FILE, "a") as file:
        file.write(f"{acc_no},{name},{balance},{contact},active\n")
    
    print("Account successfully created!")

def process_deposit():
    """Process a deposit transaction."""
    customers = read_customers()
    acc_no = input("Enter account number: ")
    
    if acc_no not in customers:
        print("Account not found!")
        return

    try:
        amount = float(input("Enter deposit amount: "))
        if amount <= 0:
            print("Invalid deposit amount!")
            return
    except ValueError:
        print("Invalid amount format!")
        return

    customers[acc_no]['balance'] += amount
    write_customers(customers)
    print("Deposit successful!")

def process_withdrawal():
    """Process a withdrawal transaction."""
    customers = read_customers()
    acc_no = input("Enter account number: ")

    if acc_no not in customers:
        print("Account not found!")
        return

    try:
        amount = float(input("Enter withdrawal amount: "))
        if amount <= 0:
            print("Invalid withdrawal amount!")
            return
    except ValueError:
        print("Invalid amount format!")
        return

    if customers[acc_no]['balance'] < amount:
        print("Insufficient funds!")
        return

    customers[acc_no]['balance'] -= amount
    write_customers(customers)
    print("Withdrawal successful!")

def issue_debit_card():
    """Issue a debit card to a customer."""
    acc_no = input("Enter account number: ")
    with open(DEBIT_CARDS_FILE, "a") as file:
        file.write(f"{acc_no}\n")
    print("Debit card issued successfully!")

def manage_loan_applications():
    """Process loan applications."""
    acc_no = input("Enter account number: ")
    loan_amount = input("Enter loan amount: ")

    with open(LOAN_FILE, "a") as file:
        file.write(f"{acc_no},{loan_amount},Pending\n")

    print("Loan application submitted!")

def close_account():
    """Close a customer account."""
    customers = read_customers()
    acc_no = input("Enter account number: ")

    if acc_no not in customers:
        print("Account not found!")
        return

    with open(CLOSED_ACCOUNTS_FILE, "a") as file:
        file.write(f"{acc_no},{customers[acc_no]['name']}\n")

    del customers[acc_no]
    write_customers(customers)
    print("Account closed successfully!")

def approve_loans():
    """Approve or reject loan applications."""
    if not os.path.exists(LOAN_FILE):
        print("No loan applications found!")
        return

    updated_loans = []
    with open(LOAN_FILE, "r") as f:
        loans = [line.strip().split(",") for line in f]

    for acc_no, amount, status in loans:
        if status.lower() == "pending":
            decision = input(f"Approve (A) / Reject (R) loan for {acc_no} of ${amount}: ").strip().upper()
            status = "Approved" if decision == "A" else "Rejected"
        updated_loans.append(f"{acc_no},{amount},{status}\n")

    with open(LOAN_FILE, "w") as f:
        f.writelines(updated_loans)
    
    print("Loan approvals updated successfully.")

def generate_financial_report():
    """Generate a financial report from transactions."""
    if not os.path.exists("transactions.txt"):
        print("No transaction data found!")
        return

    total_transactions = 0
    total_amount = 0.0

    with open("transactions.txt", "r") as f:
        for line in f:
            parts = line.strip().split(",")
            total_transactions += 1
            total_amount += float(parts[1].split("$")[-1].split()[0])

    print(f"Total Transactions: {total_transactions}, Total Amount: ${total_amount:.2f}")

def handle_complaints():
    """View and resolve customer complaints."""
    if not os.path.exists(COMPLAINTS_FILE):
        print("No complaints found!")
        return

    with open(COMPLAINTS_FILE, "r") as f:
        complaints = [line.strip().split(",", 1) for line in f]

    for acc_no, complaint in complaints:
        resolution = input(f"Resolve complaint from {acc_no}: {complaint} (Y/N)? ").strip().upper()
        if resolution == "Y":
            print(f"Complaint from {acc_no} resolved.")

def monitor_performance():
    """View branch performance metrics."""
    if os.path.exists(PERFORMANCE_FILE):
        with open(PERFORMANCE_FILE, "r") as f:
            print(f.read())

def review_account_transactions():
    acc_no = input("Enter account number to review transactions: ")
    
    if not os.path.exists(TRANSACTION_FILE):
        print("No transactions found!")
        return

    print("\nTransaction History:")
    found = False
    with open(TRANSACTION_FILE, "r") as file:
        for line in file:
            trans_acc, transaction = line.strip().split(",", 1)
            if trans_acc == acc_no:
                print(transaction)
                found = True
    
    if not found:
        print("No transactions found for this account.")

def flag_suspicious_activity():
    try:
        threshold = float(input("Enter suspicious transaction amount threshold: "))
    except ValueError:
        print("Invalid amount! Please enter a numeric value.")
        return

    flagged_transactions = []
    
    if not os.path.exists(TRANSACTION_FILE):
        print("No transactions found!")
        return

    with open(TRANSACTION_FILE, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) > 1 and "$" in parts[1]:
                try:
                    amount = float(parts[1].split("$")[-1].split()[0])
                    if amount > threshold:
                        flagged_transactions.append(line.strip())
                except ValueError:
                    continue

    if flagged_transactions:
        print("\nFlagged Suspicious Transactions:")
        for txn in flagged_transactions:
            print(txn)
        
        with open(FLAGGED_TRANSACTIONS_FILE, "w") as file:
            file.writelines([f"{txn}\n" for txn in flagged_transactions])

        print("Flagged transactions saved to file.")
    else:
        print("No suspicious transactions detected.")

def generate_audit_reports():
    if not os.path.exists(TRANSACTION_FILE):
        print("No transactions found!")
        return

    with open(TRANSACTION_FILE, "r") as file:
        transactions = file.readlines()
    
    with open(AUDIT_REPORT_FILE, "w") as report:
        report.writelines(transactions)

    print("Audit report generated successfully!")

def verify_compliance():
    if not os.path.exists(FLAGGED_TRANSACTIONS_FILE):
        print("No flagged transactions found. Compliance check clear.")
        return

    with open(FLAGGED_TRANSACTIONS_FILE, "r") as file:
        flagged = file.readlines()
    
    if flagged:
        print("\nCompliance Issues Detected:")
        for issue in flagged:
            print(issue.strip())
    else:
        print("No compliance issues found.")

def provide_improvement_suggestions():
    print("\nSuggested Improvements:")
    print("1. Implement stricter transaction limits.")
    print("2. Enhance fraud detection mechanisms.")
    print("3. Conduct regular account reviews.")
    print("4. Improve customer verification methods.")

def customer_menu():
    while True:
        print("\nBanking System - Customer Menu")
        print("1. Check Balance")
        print("2. Transfer Funds")
        print("3. Pay Bills")
        print("4. Request Account Statement")
        print("5. Update Contact Details")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            acc_no = input("Enter Account Number: ")
            check_balance(acc_no)
        elif choice == "2":
            sender = input("Enter Your Account Number: ")
            receiver = input("Enter Receiver's Account Number: ")
            amount = input("Enter Amount: ")
            transfer_funds(sender, receiver, amount)
        elif choice == "3":
            acc_no = input("Enter Account Number: ")
            biller = input("Enter Biller Name: ")
            amount = input("Enter Amount: ")
            pay_bill(acc_no, amount, biller)
        elif choice == "4":
            acc_no = input("Enter Account Number: ")
            request_statement(acc_no)
        elif choice == "5":
            acc_no = input("Enter Account Number: ")
            new_contact = input("Enter New Contact Details: ")
            update_contact(acc_no, new_contact)
        elif choice == "6":
            print("Exiting... Thank you!")
            break
        else:
            print("Invalid choice! Please try again.")

def bank_teller_menu():
    while True:
        print("\nBank Teller Menu:")
        print("1. Open New Account")
        print("2. Process Deposit")
        print("3. Process Withdrawal")
        print("4. Issue Debit Card")
        print("5. Manage Loan Applications")
        print("6. Close Account")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            open_new_account()
        elif choice == "2":
            process_deposit()
        elif choice == "3":
            process_withdrawal()
        elif choice == "4":
            issue_debit_card()
        elif choice == "5":
            manage_loan_applications()
        elif choice == "6":
            close_account()
        elif choice == "7":
            print("Exiting Bank Teller Menu.\n")
            break
        else:
            print("Invalid choice! Please try again.")

def manager_menu():
    while True:
        print("\nManager Menu:")
        print("1. Approve Loan Applications")
        print("2. Generate Financial Report")
        print("3. Handle Customer Complaints")
        print("4. Monitor Branch Performance")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            approve_loans()
        elif choice == "2":
            generate_financial_report()
        elif choice == "3":
            handle_complaints()
        elif choice == "4":
            monitor_performance()
        elif choice == "5":
            print("Exiting Manager Menu.")
            break
        else:
            print("Invalid choice! Please try again.")

def auditor_menu():
    while True:
        print("\nAuditor Menu:")
        print("1. Review Account Transactions")
        print("2. Flag Suspicious Activity")
        print("3. Generate Audit Reports")
        print("4. Verify Compliance with Policies")
        print("5. Provide Improvement Suggestions")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            review_account_transactions()
        elif choice == "2":
            flag_suspicious_activity()
        elif choice == "3":
            generate_audit_reports()
        elif choice == "4":
            verify_compliance()
        elif choice == "5":
            provide_improvement_suggestions()
        elif choice == "6":
            print("Exiting Auditor Menu.")
            break
        else:
            print("Invalid choice, please try again.")

def main():
    initialize_files()
    while True:
        print("\nMain Menu:")
        print("1. Customer Menu")
        print("2. Bank Teller Menu")
        print("3. Manager Menu")
        print("4. Auditor Menu")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            customer_menu()
        elif choice == "2":
            bank_teller_menu()
        elif choice == "3":
            manager_menu()
        elif choice == "4":
            auditor_menu()
        elif choice == "5":
            print("Exiting... Thank you!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
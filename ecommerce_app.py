import os
import re
import random
import string
from typing import Dict, List, Optional

# ---------- CONSTANTS ----------
DATA_DIR: str = "data"
ACCOUNTS_FILE: str = os.path.join(DATA_DIR, "accounts.log")
WAREHOUSE_FILES: List[str] = [f for f in os.listdir(DATA_DIR) if f.startswith("warehouse")]

# ---------- GLOBAL VARIABLES ----------
inventory: Dict[str, Dict[str, int]] = {}  # Product name -> {"price": int, "stock": int}
current_user: Optional[Dict[str, any]] = None  # Stores the signed-in user's data
cart: Dict[str, int] = {}  # Product name -> Quantity

# ---------- UTILITY FUNCTIONS ----------

def load_inventory() -> None:
    """
    Load product data from warehouse files into the global inventory dictionary.

    Reads all files in the DATA_DIR folder with names starting with "warehouse",
    parses product names and prices separated by a colon and semicolon,
    and initializes each product's stock to 10 by default.

    Side Effects:
        Updates the global 'inventory' dictionary with product details:
        {
            product_name (str): {
                "price": int,
                "stock": int
            }
        }

    Raises:
        FileNotFoundError: If warehouse files are missing.
        ValueError: If product price conversion to int fails.
    """
    global inventory
    for file_name in WAREHOUSE_FILES:
        with open(os.path.join(DATA_DIR, file_name), 'r', encoding='utf-8') as f: # This tells Python to read the file using UTF-8 encoding
        # which ensures it can correctly interpret characters from any language or symbol set that might be used in the file
            raw_data = f.read().strip()
            items = raw_data.split(";")
            for item in items:
                if ":" in item:
                    name, price = item.strip().split(":", 1)
                    inventory[name.strip()] = {
                        "price": int(price.strip()),
                        "stock": 10  # Default initial stock
                    }

def ensure_data_files() -> None:
    """
    Ensure that the data directory and accounts file exist.

    Creates the DATA_DIR directory if it does not exist, and creates an
    empty ACCOUNTS_FILE if it is missing.

    Side Effects:
        Creates necessary files/directories on disk for application data storage.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(ACCOUNTS_FILE):
        open(ACCOUNTS_FILE, 'a').close()

def validate_password(pw: str) -> bool:
    """
    Validate if a password string meets security requirements.

    Args:
        pw (str): The password string to validate.

    Returns:
        bool: True if the password satisfies all criteria; False otherwise.

    Criteria:
        - Minimum length of 8 characters.
        - Contains at least one lowercase letter.
        - Contains at least one uppercase letter.
        - Contains at least one digit.
        - Contains at least one special character (punctuation).
    """
    return (
        len(pw) >= 8 and
        any(c.islower() for c in pw) and
        any(c.isupper() for c in pw) and
        any(c.isdigit() for c in pw) and
        any(c in string.punctuation for c in pw)
    )

def generate_password() -> str:
    """
    Generate a strong random password of length 20 that meets security criteria.

    Uses uppercase letters, lowercase letters, digits, and punctuation marks.
    The password is repeatedly generated until it passes `validate_password`.

    Returns:
        str: A randomly generated strong password string.
    """
    while True:
        pw = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=20))
        if validate_password(pw):
            return pw

def load_accounts() -> List[Dict[str, any]]:
    """
    Load user account data from the accounts log file.

    Parses each line of the ACCOUNTS_FILE, expecting a CSV format:
    username,email,password,balance

    Returns:
        List[Dict[str, any]]: A list of user account dictionaries, each containing:
            - "username" (str): The user's username.
            - "email" (str): The user's email address.
            - "password" (str): The user's password.
            - "balance" (float): The user's account balance.

    Raises:
        FileNotFoundError: If ACCOUNTS_FILE does not exist.
        ValueError: If balance conversion to float fails or line is malformed.
    """
    users: List[Dict[str, any]] = []
    with open(ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                username, email, password, balance = line.strip().split(",")
                users.append({
                    "username": username.strip(),
                    "email": email.strip(),
                    "password": password.strip(),
                    "balance": float(balance.strip())
                })
    return users


def save_accounts(users: List[Dict[str, any]]) -> None:
    """
    Save the list of user accounts to the accounts log file.

    Overwrites the existing ACCOUNTS_FILE with updated user data.

    Args:
        users (List[Dict[str, any]]): List of user account dictionaries to save.
            Each dictionary must contain keys: "username", "email", "password", "balance".

    Side Effects:
        Writes to the ACCOUNTS_FILE on disk.
    """
    with open(ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
        for user in users:
            f.write(f"{user['username']},{user['email']},{user['password']},{user['balance']:.2f}\n")

# ---------- AUTHENTICATION ----------

def sign_up() -> None:
    """
    Handle new user registration via console input.

    Prompts the user to input a unique username and email, and either
    manually input a strong password or generate one automatically.

    Side Effects:
        Updates the accounts file with the new user's data.
        Prints status messages and password info to the console.
    """
    print("\n--- Sign Up ---")
    users = load_accounts()
    usernames = [u['username'] for u in users]
    emails = [u['email'] for u in users]

    while True:
        username = input("Enter a username: ").strip()
        if username in usernames:
            print("Username already exists. Try again.")
        else:
            break

    while True:
        email = input("Enter an email: ").strip()
        if email in emails:
            print("Email already exists. Try again.")
        else:
            break

    method = input("Enter '1' to manually enter password, or '2' to generate: ").strip()
    if method == "1":
        while True:
            pw = input("Enter a strong password: ").strip()
            if validate_password(pw):
                break
            else:
                print("Password doesn't meet requirements.")
    else:
        pw = generate_password()
        print(f"Generated password: {pw}")

    users.append({
        "username": username,
        "email": email,
        "password": pw,
        "balance": 0.00
    })
    save_accounts(users)
    print("Account created successfully!")

def sign_in() -> bool:
    """
    Authenticate a user by prompting for username/email and password.

    Compares input credentials against stored accounts. If a match is found,
    stores the authenticated user's data in the global 'current_user'.

    Returns:
        bool: True if authentication is successful; False otherwise.

    Side Effects:
        Updates the global 'current_user' dictionary on successful login.
        Prints welcome or error messages to the console.
    """
    global current_user
    print("\n--- Sign In ---")
    users = load_accounts()
    id_ = input("Enter username or email: ").strip()
    pw = input("Enter password: ").strip()

    for user in users:
        if (user["username"] == id_ or user["email"] == id_) and user["password"] == pw:
            current_user = user
            print(f"Welcome back, {current_user['username']}!")
            return True
    print("Invalid credentials.")
    return False

def forget_password() -> None:
    """
    Allow a user to reset their password by verifying their registered email.

    Prompts for email, then allows either manual password entry or
    auto-generation of a strong password. Updates the accounts file upon success.

    Side Effects:
        Modifies the password for the specified user in the accounts file.
        Prints status messages and new password details to the console.
    """
    print("\n--- Forget Password ---")
    users = load_accounts()
    email = input("Enter your registered email: ").strip().lower()
    for user in users:
        if user['email'] == email:
            method = input("Enter '1' to manually enter password, or '2' to generate: ").strip()
            if method == "1":
                while True:
                    new_pw = input("Enter a strong password: ").strip()
                    if validate_password(new_pw):
                        user['password'] = new_pw
                        save_accounts(users)
                        print(f"Password reset successful! Your new password is: {new_pw}")
                        break
                    else:
                        print("Password doesn't meet requirements.")
            elif method == "2":
                new_pw = generate_password()
                user['password'] = new_pw
                save_accounts(users)
                print(f"Password reset successful! Your new password is: {new_pw}")
            return
    print("Email not found.")

# ---------- WALLET AND SHOPPING ----------

def fund_wallet() -> None:
    """
    Allow the authenticated user to add funds to their wallet balance.

    Presents fixed funding options, updates the user's balance, and
    saves the updated data to the accounts file.

    Side Effects:
        Updates global 'current_user' balance and persists changes to disk.
        Prints funding options and transaction result messages.
    """
    print("\n--- Fund Wallet ---")
    options: Dict[str, int] = {
        "1": 10000,
        "2": 20000,
        "3": 50000,
        "4": 100000
    }
    for k, v in options.items():
        print(f"{k}. NGN {v:,}")

    choice = input("Choose amount to fund: ").strip()
    if choice in options:
        amount = options[choice]
        current_user['balance'] += amount
        print(f"NGN {amount:,} added to wallet. New balance: NGN {current_user['balance']:.2f}")
        users = load_accounts()
        for user in users:
            if user['username'] == current_user['username']:
                user['balance'] = current_user['balance']
        save_accounts(users)
    else:
        print("Invalid choice.")

def manage_account() -> None:
    """
    Present account management options to the authenticated user.

    Allows the user to:
        - View wallet balance.
        - Change username (must be unique).
        - Change password (must meet security criteria).
        - View profile details (username, email, balance).
        - Delete their account after confirmation.
        - Exit account management menu.

    Side Effects:
        Updates 'current_user' and accounts file based on user's choices.
        Can result in user account deletion and logout.
        Prints interactive prompts and status messages.
    """
    global current_user
    while True:
        print("\n--- Manage Account ---")
        print("1. View Balance")
        print("2. Change Username")
        print("3. Change Password")
        print("4. View Profile")
        print("5. Delete Account")
        print("6. Exit Manage Account")
        choice = input("Choose an option: ").strip()

        users = load_accounts()
        user_index = next((i for i, u in enumerate(users) if u['username'] == current_user['username']), -1)
        if user_index == -1:
            print("Error: Current user not found.")
            break

        if choice == "1":
            print(f"Balance: NGN {current_user['balance']:.2f}")
        elif choice == "2":
            new_name = input("Enter new username: ").strip()
                        if any(u['username'] == new_name for u in users):
    print("Username already taken.")
            else:
                users[user_index]['username'] = new_name
                current_user['username'] = new_name
                save_accounts(users)
                print("Username updated.")
        elif choice == "3":
            while True:
                new_pw = input("Enter new password: ").strip()
                if validate_password(new_pw):
                    users[user_index]['password'] = new_pw
                    current_user['password'] = new_pw
                    save_accounts(users)
                    print("Password updated.")
                    break
                else:
                    print("Password doesn't meet security requirements.")
        elif choice == "4":
            print(f"Username: {current_user['username']}")
            print(f"Email: {current_user['email']}")
            print(f"Balance: NGN {current_user['balance']:.2f}")
        elif choice == "5":
            confirm = input("Are you sure you want to delete your account? (y/n): ").strip().lower()
            if confirm == 'y':
                del users[user_index]
                save_accounts(users)
                current_user = None
                print("Account deleted. Logging out.")
                break
        elif choice == "6":
            break
        else:
            print("Invalid option.")

def search_inventory() -> None:
    """
    Enable the user to search for products in the inventory by keywords.

    Performs case-insensitive substring matching on product names.
    Displays matched items with their prices and stock.
    Allows adding a selected item to the global shopping cart, if in stock.

    Side Effects:
        Updates 'cart' dictionary with selected item quantities.
        Updates 'inventory' stock levels accordingly.
        Prints search results and status messages to the console.
    """
    print("\n--- Search Products ---")
    query = input("Search for an item: ").strip()
    terms = query.split()
    patterns = [re.compile(re.escape(term), re.IGNORECASE) for term in terms]
    results = [item for item in inventory if all(p.search(item) for p in patterns)]

    if not results:
        print("No items matched your search.")
        return

    print("\nMatched Items:")
    for i, item in enumerate(results, 1):
        data = inventory[item]
        print(f"{i}. {item} - Price: NGN {data['price']:,} - Stock: {data['stock']}")

    choice = input("Enter number to add to cart or 'x' to exit: ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(results):
            item = results[idx]
            if inventory[item]['stock'] > 0:
                cart[item] = cart.get(item, 0) + 1
                inventory[item]['stock'] -= 1
                print(f"{item} added to cart.")
            else:
                print(f"{item} is out of stock.")
        else:
            print("Invalid item number.")
    elif choice.lower() != 'x':
        print("Invalid input.")

def view_cart() -> None:
    """
    Display the contents of the user's shopping cart with quantities, prices, and subtotal.

    Prints each item's name, quantity, individual price, subtotal for the item,
    and the total cost of all items in the cart.

    If the cart is empty, notifies the user accordingly.
    """
    print("\n--- Your Cart ---")
    if not cart:
        print("Cart is empty.")
        return

    total: int = 0
    for i, (item, qty) in enumerate(cart.items(), 1):
        price = inventory[item]['price']
        subtotal = price * qty
        total += subtotal
        print(f"{i}. {item} - Qty: {qty} - Price: {price:,} = NGN {subtotal:,}")

    print(f"Total: NGN {total:,}")

def manage_cart() -> None:
    """
    Provide an interactive menu for managing the shopping cart.

    Options include:
        - Viewing current cart contents.
        - Removing specific items by name (restores stock).
        - Clearing the entire cart (restores stock).
        - Exiting the cart management menu.

    Side Effects:
        Updates global 'cart' and 'inventory' dictionaries.
        Prints menu and status messages.
    """
    while True:
        print("\n--- Manage Cart ---")
        print("1. View Cart")
        print("2. Remove Item")
        print("3. Clear Cart")
        print("4. Exit Manage Cart")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_cart()
        elif choice == "2":
            if not cart:
                print("Cart is empty.")
                continue
            view_cart()
            item_name = input("Enter item name to remove: ").strip()
            if item_name in cart:
                removed_qty = cart.pop(item_name)
                inventory[item_name]['stock'] += removed_qty
                print(f"{item_name} removed from cart and {removed_qty} restored to stock.")
            else:
                print("Item not found in cart.")
        elif choice == "3":
            for item_name, qty in cart.items():
                inventory[item_name]['stock'] += qty
            cart.clear()
            print("Cart has been cleared and stock restored.")
        elif choice == "4":
            break
        else:
            print("Invalid option.")

def checkout() -> None:
    """
    Complete the purchase process for all items in the shopping cart.

    Calculates the total price of items in the cart and prompts the user
    to confirm payment. Checks if the current user has sufficient balance.

    On successful payment:
        - Deducts total amount from user's balance.
        - Clears the shopping cart.
        - Updates the accounts file with new balance.
        - Prints confirmation message.

    On failure:
        - Prints an error message for insufficient funds or cancellation.

    Side Effects:
        Modifies global 'current_user' balance, updates persistent storage,
        and clears 'cart'.
    """
    print("\n--- Checkout ---")
    if not cart:
        print("Cart is empty.")
        return

    total = sum(inventory[item]['price'] * qty for item, qty in cart.items())
    print(f"Total amount: NGN {total:,}")
    confirm = input("Proceed to pay? (y/n): ").strip().lower()
    if confirm == 'y':
        if current_user['balance'] >= total:
            current_user['balance'] -= total
            cart.clear()
            users = load_accounts()
            for user in users:
                if user['username'] == current_user['username']:
                    user['balance'] = current_user['balance']
            save_accounts(users)
            print("Payment successful! Thank you for your purchase.")
        else:
            print("Insufficient balance.")
    else:
        print("Checkout cancelled.")

# ---------- MAIN MENU AND APPLICATION ENTRY ----------

def run_menu() -> None:
    """
    Display the main menu after user login and process menu selections.

    Options include:
        1. Fund Wallet
        2. Manage Account
        3. Search for Items
        4. View Cart
        5. Manage Cart
        6. Checkout
        7. Logout

    Loops until the user chooses to log out.

    Side Effects:
        Executes corresponding functions based on user input.
    """
    while True:
        print(f"\nWelcome, {current_user['username']}! Choose an option:")
        print("1. Fund Wallet")
        print("2. Manage Account")
        print("3. Search for Items")
        print("4. View Cart")
        print("5. Manage Cart")
        print("6. Checkout")
        print("7. Logout")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            fund_wallet()
        elif choice == "2":
            manage_account()
            if current_user is None:
                # User deleted account or logged out
                break
        elif choice == "3":
            search_inventory()
        elif choice == "4":
            view_cart()
        elif choice == "5":
            manage_cart()
        elif choice == "6":
            checkout()
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")

def main() -> None:
    """
    Main program entry point.

    Initializes data files and inventory, presents initial menu for sign-in,
    sign-up, or password reset.

    Upon successful login, enters the main menu loop.

    Side Effects:
        Manages global variables and prints to the console.
    """
    ensure_data_files()
    load_inventory()

    while True:
        print("\nWelcome! Choose an option:")
        print("1. Sign In")
        print("2. Sign Up")
        print("3. Forget Password")
        print("4. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            if sign_in():
                run_menu()
        elif choice == "2":
            sign_up()
        elif choice == "3":
            forget_password()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()

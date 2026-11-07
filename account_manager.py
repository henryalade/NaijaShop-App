def manage_account(user, accounts):
    while True:
        print("\n--- Account Management ---")
        print("1. Change Username")
        print("2. Change Email")
        print("3. Change Password")
        print("4. View Account Details")
        print("5. Reset Balance")
        print("6. Delete Account")
        print("7. Logout")
        print("8. Exit to Main Menu")
        choice = input("Choose an option: ")

        if choice == "1":
            change_username(user, accounts)
        elif choice == "2":
            change_email(user, accounts)
        elif choice == "3":
            change_password(user, accounts)
        elif choice == "4":
            view_account_details(user)
        elif choice == "5":
            reset_balance(user, accounts)
        elif choice == "6":
            if delete_account(user, accounts):
                return "logout"
        elif choice == "7":
            return "logout"
        elif choice == "8":
            break
        else:
            print("Invalid option. Please try again.")

# change username
def change_username(user, accounts):
    current_password = input("Please Enter your password to confirm: ")
    if current_password != user['password']:
        print("Incorrect password.")
        return

    new_username = input("Kindly Enter new username: ")
    if any(acc['username'] == new_username for acc in accounts):
        print("This username already exists.")
        return

    user['username'] = new_username
    print("Username was successfully updated.")

#change email
def change_email(user, accounts):
    password = input("Please Enter your password to confirm: ")
    if password != user["password"]:
        print("❌ Incorrect password.")
        return

    new_email = input("Kindly Enter your new email: ")
    if any(acc["email"] == new_email for acc in accounts):
        print("❌ Email already in use.")
        return

    user["email"] = new_email
    print("✅ Email was successfully updated.")

#change password
def change_password(user):
    old_password = input("Kindly Enter current password: ")
    # Ensure old password matches before proceeding
    if old_password != user["password"]:
        print("❌ Incorrect current password.")
        return

    new_password = input("Enter new password: ")

    # Validate password strength
    if len(new_password) < 16 or \
       not any(c.islower() for c in new_password) or \
       not any(c.isupper() for c in new_password) or \
       not any(c.isdigit() for c in new_password) or \
       not any(not c.isalnum() for c in new_password):
        print("❌ Your Password must be at least 16 characters long and should include uppercase, lowercase, number, and symbol.")
        return

    # Update password
    user["password"] = new_password
    print("✅ Password change was successfully.")

# Function to show the user's account details
def view_account_details(user):
    password = input("Please Enter your password to confirm: ")
    # Verify password before showing details
    if password != user["password"]:
        print("❌ Incorrect password.")
        return

    # Print user information
    print("\n--- Account Details ---")
    print(f"Username: {user['username']}")
    print(f"Email: {user['email']}")
    print(f"Balance: ₦{user['balance']}")


# Function to delete a user account
def delete_account(user, accounts):
    password = input("Please Enter your password to confirm: ")
    # Make sure only the real user can delete account
    if password != user["password"]:
        print("❌ Incorrect password.")
        return False

    confirm = input("Are you sure you want to delete your account permanently? (yes/no): ").lower()
    if confirm == "yes":
        # Remove the user from the accounts list
        accounts.remove(user)
        print("✅ Account successfully deleted.")
        return True
    else:
        print("❌ Account deletion cancelled.")
        return False









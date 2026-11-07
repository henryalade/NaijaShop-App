import random
import string

class User:
    def _init_(self, username, password):
        self.username = username
        self.password = password


users = []
current_user = None


def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def sign_up():
    username = input("Create a username: ")

    choice = input("Do you want to use a generated password? (yes/no): ").strip().lower()
    if choice == "yes":
        password = generate_password()
        print(f"Your generated password is: {password}")
    else:
        password = input("Create your own password: ")

    for user in users:
        if user.username == username:
            print("Username already exists.")
            return

    users.append(User(username, password))
    print("Sign-up successful!")


def send_auth_code():
    code = str(random.randint(1000, 9999))
    print(f"(Your authentication code is: {code})")  # In real apps, this would be private
    return code


def login():
    global current_user
    username = input("Username: ")
    password = input("Password: ")

    for user in users:
        if user.username == username and user.password == password:
            auth_code = send_auth_code()
            entered_code = input("Enter the authentication code: ")
            if entered_code == auth_code:
                current_user = user
                print(f"Login successful! Welcome {current_user.username}")
            else:
                print("Invalid authentication code.")
            return

    print("Invalid username or password.")


def logout():
    global current_user
    if current_user:
        print(f"{current_user.username} logged out.")
        current_user = None
    else:
        print("No user is logged in.")


def main():
    while True:
        print("\n1. Sign Up\n2. Login\n3. Logout\n4. Exit")
        option = input("Choose an option: ")

        if option == "1":
            sign_up()
        elif option == "2":
            login()
        elif option == "3":
            logout()
        elif option == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid input.")


if _name_ == "_main_":
    main()
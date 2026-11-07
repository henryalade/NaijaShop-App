
# utils.py

def display_cart(cart):
    if not cart:
        print("You haven't entered any cart.")
    else:
        print("Shopping Cart ")
        total_cost = 0
        for i, item in enumerate(cart, start=1):
            print(f"{i}. {item['name']}: ₦{item['price']}")
            total_cost += item['price']
        print(f"Total cost: ₦{total_cost:.2f}")

def get_item_input():
    name = input("Enter Item Name: ")
    try:
        price = float(input("Enter Item Price: "))
        return {"name": name, "price": price}
    except ValueError:
        print("Invalid price entered. Please try again.")
        return None

def remove_item(cart):
    display_cart(cart)
    try:
        index = int(input("Enter the Item number you would like to remove 🗑: ")) - 1
        if 0 <= index < len(cart):
            removed = cart.pop(index)
            print(f"Item removed: {removed['name']}")
        else:
            print(" Item number out of range.")
    except ValueError:
        print(" Please enter a valid number.")

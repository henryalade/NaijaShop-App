def display_cart(cart):
    if not cart:
        print("You haven't entered any cart.")
    else:
        print("shopping cart")
    total_cost = 0
    for items in cart:
        print(f"{items['name']}: ₦{items['price']}")
        total_cost += items['price']
    print(f"Total cost: ₦{total_cost:.2f}")

def main():
    cart = []
    while True:
        print("\nWelcome to the cart!🛒")
        print("1. Add Item To Cart➕")
        print("2. Display Cart📺")
        print("3.Remove Item From Cart🚮")
        print("4. Exit🏃‍♀‍➡")

        choice = input("Enter your choice: ")
        if choice == "1":
            Item_name = input("Enter Item Name: ")
            Item_price = float(input("Enter Item Price: "))
            Item = {"name": Item_name, "price": Item_price}
            cart.append(Item)
            print(f"Item added to the cart: {Item}")
        elif choice == "2":
            display_cart(cart)
        elif choice == "3":
            if not cart:
                print("You haven't entered any cart.")
            else:
                display_cart(cart)
                item_index = int(input("Enter the Item number you would like to remove 🗑: ")) - 1
                if 0 <= item_index < len(cart):
                    removed_item = cart.pop(item_index)
                    print(f"Item removed: {removed_item['name']}")
                else:
                    print("❌Item not found in cart.")
        elif choice == "4":
            print("👋Thank you for your time!")
            break
        else:
            print("Invalid choice please enter a valid choice.")


if _name_ == "_main_":
    main()

# Imports
from crud import create_customer, create_order, create_product, get_customers, get_orders, get_products, get_session, update_product_price, del_customer

# Interaction
def make_customer():
    name = input("Enter customer name: ")
    email = input("Enter customer email: ")
    create_customer(name, email)
    print(f"Customer {name} created!")

def make_product():
    name = input("Enter order name: ")
    price = float(input("Enter order price: "))
    stock = int(input("Enter order stock: "))
    create_product(name, price, stock)
    print(f"Order {name} with {stock} stock added!")

def make_order():
    cusomer_id = int(input("Enter customer ID: "))
    product_quantities = {}

    while True:
        product_name = input("Enter product name (or done to finish): ")
        if product_name == "done":
            break
        quantity = int(input("Enter quantity for {product_name}: "))
        product_quantities[product_name] = quantity

    try:
        create_order(cusomer_id,product_quantities)
        print(f"Order created of Customer ID: {cusomer_id} for {product_name}")
    except Exception as e:
        print(f"Failed to create order: {e}")

# Main Function
def main():
    while True:
        print("===Store Management System")
        print("1. Create Customer")
        print("2. Add Product")
        print("3. Create Order")
        print("4. View existing Customers")
        print("5. View existing Products")
        print("6. View existing Orders")
        print("7. Update existing Products")
        print("8. Delete a Customer")
        print("9. Exit")

        option = int(input("Select a option(1-9) from the above: "))

        if option == 1:
            make_customer()
        elif option == 2:
            make_product()
        elif option == 3:
            make_order()
        elif option == 4:
            print("Customers: ",get_customers())
        elif option == 5:
            print("Products: ",get_products())
        elif option == 6:
            print("Orders: ",get_orders())
        elif option == 7:
            product_id = int(input("Product id: "))
            price = float(input("New Price: "))
            update_product_price(product_id, price)
            get_orders()
        elif option == 8:
            customer_id = int(input("Customer ID: "))
            del_customer(customer_id)
            get_customers()
        elif option == 9:
            print("Existing...")
            break
        else:
            print("Invalid input!")

if __name__ == "__main__":
    main()
# CRUD operations

# Imports
    # Self Created Package
from db import get_session 
from models import Customer,Product,Order,OrderItem

# Create Operations(Customer, Products, Orders)
def create_customer(name:str, email:str) -> None:
    session = get_session()
    new_customer = Customer(name=name, email=email)
    session.add(new_customer)
    session.commit()
    session.close()

def create_product(name:str, price:float, stock:int) -> None:
    session = get_session()
    new_product = Product(name=name,price=price,stock=stock)
    session.add(new_product)
    session.commit()
    session.close()

def create_order(customer_id: int, product_quantities: dict[str, int]) -> None:
    session = get_session()

    # Fetch all products and store them in a dictionary with lowercase names as keys
    products = {product.name.lower(): product for product in session.query(Product).all()}
    
    # Create order
    order = Order(customer_id=customer_id, total_amount=0)  # Initialize total_amount as 0
    session.add(order)
    session.commit()

    total_amount = 0
    
    # Process the order items based on product names
    for product_name, quantity in product_quantities.items():
        product_name_lower = product_name.lower()  # Convert the entered product name to lowercase
        if product_name_lower in products:
            product = products[product_name_lower]
            order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=quantity)
            session.add(order_item)

            # Update total amount
            total_amount += product.price * quantity
        else:
            print(f"Product '{product_name}' not found!")
    
    # Update the order with the calculated total amount
    order.total_amount = total_amount
    session.commit()

    session.close()
    print(f"Order created for Customer ID: {customer_id} with total amount: {total_amount}")


# Read Operations(Customer, Products, Orders)
def get_customers():
    session = get_session()
    customers = session.query(Customer).all()
    session.close()
    return customers

def get_products():
    session = get_session()
    products = session.query(Product).all()
    session.close()
    return products

def get_orders():
    session = get_session()
    orders = session.query(Order).all()
    session.close()
    return orders

# Update Operations(Products price)
def update_product_price(product_id:int, new_price:float) -> None:
    session = get_session()
    product = session.query(Product).filter_by(Product.id == product_id).first()
    if product:
        product.price = new_price
        session.commit(product)

    session.close()

# Delete Operation(Customer)
def del_customer(customer_id:int) -> None:
    session = get_session()
    customer = session.query(Customer).filter_by(Customer.id == customer_id).first()
    if customer:
        session.delete(customer)
        session.commit()
    session.close()
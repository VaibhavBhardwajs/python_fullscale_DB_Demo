# Models for DataBase

# Imports
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Base Class
Base = declarative_base()

# Defining Models
    # Customer Model
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    orders = relationship('Order', back_populations='customer')

    def __repr__(self):
        return f"<Customer(id={self.id}, name={self.name}, email={self.email})>"
    
    # Product Model
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    stock = Column(Integer)

    order_items = relationship('OrderItem',back_populations='prouduct')

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, stock={self.stock})>"
    
    # Order Model
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    total_amount = Column(Float)

    # Relationship
    customer = relationship('Customer',back_populations='orders')
    order_items = relationship('OrderItem',back_populations='order')

    def __repr__(self):
        return f"<Order(id={self.id}, customer_id={self.customer_id}, total_amount={self.total_amount})>"
    
    # Order Item Model
class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    # Relationship
    order = relationship('Order',back_populations='order_items')
    product = relationship('Product',back_populations='order_items')

    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"
    
# Imports 
from crud import create_customer, create_order, create_product, get_customers, get_orders, get_products, update_product_price, update_product_stock, del_customer
from db import get_session
from models import Order, OrderItem 
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QWidget, QComboBox, QPushButton, QTableWidget, QVBoxLayout, 
                             QHBoxLayout, QMessageBox, QTableWidgetItem, QHeaderView, QDialog, QLabel, QLineEdit, 
                             QSpinBox, QDoubleSpinBox, QDialogButtonBox)

# Custom Dialog for Customer Input
class CustomerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Customer")
        self.setGeometry(300, 300, 300, 150)
        self.layout = QVBoxLayout()

        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_input)

        # Dialog buttons (OK and Cancel)
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_inputs(self):
        return self.name_input.text(), self.email_input.text()

# Custom Dialog for Product Input
class ProductDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Product")
        self.setGeometry(300, 300, 300, 200)
        self.layout = QVBoxLayout()

        self.name_label = QLabel("Product Name:")
        self.name_input = QLineEdit()
        self.price_label = QLabel("Price:")
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 100000)
        self.stock_label = QLabel("Stock:")
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 10000)

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.price_label)
        self.layout.addWidget(self.price_input)
        self.layout.addWidget(self.stock_label)
        self.layout.addWidget(self.stock_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_inputs(self):
        return self.name_input.text(), self.price_input.value(), self.stock_input.value()

class UpdateProductDialog(QDialog):
    def __init__(self, product):
        super().__init__()
        self.setWindowTitle(f"Update Product: {product.name}")
        self.setGeometry(300, 300, 300, 200)
        self.layout = QVBoxLayout()

        self.name_label = QLabel("Product Name:")
        self.name_input = QLineEdit(product.name)  # Pre-fill the current name

        self.price_label = QLabel("Price:")
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 100000)
        self.price_input.setValue(product.price)  # Pre-fill the current price

        self.stock_label = QLabel("Stock:")
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 10000)
        self.stock_input.setValue(product.stock)  # Pre-fill the current stock

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.price_label)
        self.layout.addWidget(self.price_input)
        self.layout.addWidget(self.stock_label)
        self.layout.addWidget(self.stock_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_inputs(self):
        return self.name_input.text(), self.price_input.value(), self.stock_input.value()


# Custom Dialog for Order Input
class OrderDialog(QDialog):
    def __init__(self, products):
        super().__init__()
        self.setWindowTitle("Add Order")
        self.setGeometry(300, 300, 300, 200)
        self.layout = QVBoxLayout()

        # Customer selection with ComboBox
        self.customer_label = QLabel("Customer:")
        self.customer_combo = QComboBox()
        self.populate_customers()  # Populate the ComboBox with customers

        # Product selection with ComboBox
        self.product_label = QLabel("Product:")
        self.product_combo = QComboBox()
        self.populate_products(products)  # Populate the ComboBox with products from the argument

        # Quantity selection
        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 1000)

        # Layout setup
        self.layout.addWidget(self.customer_label)
        self.layout.addWidget(self.customer_combo)
        self.layout.addWidget(self.product_label)
        self.layout.addWidget(self.product_combo)
        self.layout.addWidget(self.quantity_label)
        self.layout.addWidget(self.quantity_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def populate_customers(self):
        customers = get_customers()
        for customer in customers:
            self.customer_combo.addItem(f"{customer.id}. {customer.name}", customer.id)  # Cosmetic display, value is ID

    def populate_products(self, products):
        for product in products:
            self.product_combo.addItem(f"{product.name}", product.name)  # Display product name
    def get_inputs(self):
        customer_id = self.customer_combo.currentData()  # Returns the customer ID
        product_name = self.product_combo.currentText()  # Returns the selected product name
        quantity = self.quantity_input.value()  # Returns the quantity input
        return customer_id, product_name, quantity





# Main App Class
class mainClass(QWidget):
    def __init__(self):
        super().__init__()
        # App objects and settings
        self.resize(400, 300)
        self.setWindowTitle("CRUD GUI Demo")
        self.setWindowIcon(QIcon("")) 

        # Create Objects
        # Add customer button
        self.add_cust = QPushButton("Add Customer")
        self.add_cust.setObjectName("add_cust")

        # Add product button
        self.add_prod = QPushButton("Add Product")
        self.add_prod.setObjectName("add_prod")

        # Add order button
        self.add_ordr = QPushButton("Add Order")
        self.add_ordr.setObjectName("add_ordr")

        self.view_box = QComboBox()
        self.view_box.addItems(["Select View", "View existing Customers", "View existing Products", "View existing Orders"])

        # Table Setup
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        header_names = ["ID", "Name", "Email/Price/Quantity", "Stock/Details", "Actions"]
        self.table.setHorizontalHeaderLabels(header_names)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.hide()  # Hide table initially
        self.table.hideColumn(0)

        self.setStyleSheet("""
    QWidget {
        background-color: #a2a3a2;
    }

    QLabel {
        color: #333;
        font-size: 14px;
    }

    QLineEdit, QComboBox, QDateEdit, QPushButton {
        background-color: #ede8e8;
        color: #333;
        border: 1px solid #444;
        padding: 5px;
    }

    QComboBox QAbstractItemView {
        background-color: #ede8e8;
        color: #333;
    }

    QComboBox QAbstractItemView::item:selected {
        background-color: #45a049;
        color: white;
    }

    QTableWidget {
        background-color: white;
        color: #333;
        border: 1px solid #444;
        selection-background-color: #4caf50;
    }

    QHeaderView::section {
        color: white;
        background-color: #a2a3a2;
    }

    QTableCornerButton::section {
        background-color: #a2a3a2;
    }

    /* Add Buttons: Softer Orange */
    QPushButton#add_cust, QPushButton#add_prod, QPushButton#add_ordr {
        background-color: #ffa500;
        color: #fff;
        border: none;
        padding: 8px 16px;
        font-size: 14px;
    }

    QPushButton#add_cust:hover, QPushButton#add_prod:hover, QPushButton#add_ordr:hover {
        background-color: #e69500;
    }

    /* Delete Buttons: Red */
    QPushButton#delete_btn {
        background-color: #ff4c4c;
        color: white;
        border: none;
        padding: 8px 16px;
        font-size: 14px;
    }

    QPushButton#delete_btn:hover {
        background-color: #e63b3b;
    }

    /* Update Buttons: Blue */
    QPushButton#update_btn {
        background-color: #1e90ff;
        color: white;
        border: none;
        padding: 8px 16px;
        font-size: 14px;
    }

    QPushButton#update_btn:hover {
        background-color: #1a7ed6;
    }

    /* Dialog Button Styles (OK/Cancel) */
    QDialogButtonBox QPushButton {
        background-color: #808080;  /* Neutral color for dialog buttons */
        color: white;
        border: none;
        padding: 8px 16px;
        font-size: 14px;
    }

    QDialogButtonBox QPushButton:hover {
        background-color: #666666;
    }
""")


        # App Layout
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()

        self.row1.addWidget(self.add_cust)
        self.row1.addWidget(self.add_prod)

        self.row2.addWidget(self.add_ordr)
        self.row2.addWidget(self.view_box)
        self.master_layout.addLayout(self.row1, 25)
        self.master_layout.addLayout(self.row2, 25)
        self.master_layout.addWidget(self.table)

        self.setLayout(self.master_layout)

        # Event Connections
        self.add_cust.clicked.connect(self.make_customer)
        self.add_prod.clicked.connect(self.make_product)
        self.add_ordr.clicked.connect(self.make_order)
        self.view_box.currentIndexChanged.connect(self.populate_table)

    # Functions for Interaction
    def make_customer(self):
        dialog = CustomerDialog()
        if dialog.exec():
            name, email = dialog.get_inputs()
            if name and email:
                try:
                    create_customer(name, email)
                    QMessageBox.information(self, "Success", f"Customer {name} created!")
                except ValueError as e:
                    QMessageBox.warning(self, "Duplicate Error", str(e))
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to create customer: {e}")
            else:
                QMessageBox.warning(self, "Input Error", "Please provide valid inputs.")


    def make_product(self):
        dialog = ProductDialog()
        if dialog.exec():
            name, price, stock = dialog.get_inputs()
            if name:
                create_product(name, price, stock)
                QMessageBox.information(self, "Success", f"Product {name} with {stock} stock added!")
            else:
                QMessageBox.warning(self, "Input Error", "Please provide valid inputs.")

    def make_order(self):
        products = get_products()  # Get the list of products
        dialog = OrderDialog(products)  # Pass the products to the dialog
        if dialog.exec():
            customer_id, product_name, quantity = dialog.get_inputs()
            product_quantities = {product_name: quantity}
            create_order(customer_id, product_quantities)
            QMessageBox.information(self, "Success", "Order created successfully!")




    def delete_customer(self, customer):
        # Confirmation dialog
        reply = QMessageBox.question(
            self, "Delete Customer", 
            f"Are you sure you want to delete {customer.name}?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                del_customer(customer.id)  # Call the delete function from CRUD
                QMessageBox.information(self, "Success", f"Customer {customer.name} deleted!")
                self.populate_table()  # Refresh the table after deletion
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete customer: {e}")

    def update_product(self, product):
        dialog = UpdateProductDialog(product)
        if dialog.exec():
            new_name, new_price, new_stock = dialog.get_inputs()
            try:
                # Update both the price and the stock
                update_product_price(product.id, new_price)
                update_product_stock(product.id, new_stock)
                QMessageBox.information(self, "Success", f"Product {new_name} updated!")
                self.populate_table()  # Refresh the table after update
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to update product: {e}")





    def populate_table(self):
        session = get_session()  # Make sure session is defined before querying
        orders = session.query(Order).all()

        # Clear current table contents
        self.table.setRowCount(0)

        # Fetch the selected view option
        selected_option = self.view_box.currentText()

        if selected_option == "Select View":
            self.table.hide()  # Hide table when no view is selected
            return

        self.table.show()  # Show table only if a valid view is selected

        if selected_option == "View existing Customers":
            data = get_customers()
            self.table.setColumnCount(4)  # Add one more column for delete button
            self.table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Action"])
            
            for row_idx, customer in enumerate(data):
                self.table.insertRow(row_idx)
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(customer.id)))  # Access via attribute
                self.table.setItem(row_idx, 1, QTableWidgetItem(customer.name))  # Access via attribute
                self.table.setItem(row_idx, 2, QTableWidgetItem(customer.email))  # Access via attribute

                # Create Delete Button for each customer
                delete_btn = QPushButton("Delete")
                delete_btn.setObjectName("delete_btn")  # Set object name for styling
                delete_btn.clicked.connect(lambda _, c=customer: self.delete_customer(c))  # Pass customer object
                self.table.setCellWidget(row_idx, 3, delete_btn)  # Add the button in the last column

        elif selected_option == "View existing Products":
            data = get_products()
            self.table.setColumnCount(5)  # Add one more column for update button
            self.table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Stock", "Action"])
            
            for row_idx, product in enumerate(data):
                self.table.insertRow(row_idx)
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(product.id)))  # Access via attribute
                self.table.setItem(row_idx, 1, QTableWidgetItem(product.name))  # Access via attribute
                self.table.setItem(row_idx, 2, QTableWidgetItem(f"${product.price}"))  # Access via attribute
                self.table.setItem(row_idx, 3, QTableWidgetItem(str(product.stock)))  # Access via attribute

                # Create Update Button for each product
                update_btn = QPushButton("Update")
                update_btn.setObjectName("update_btn")  # Set object name for styling
                update_btn.clicked.connect(lambda _, p=product: self.update_product(p))  # Pass product object
                self.table.setCellWidget(row_idx, 4, update_btn)  # Add the button in the last column
            
        elif selected_option == "View existing Orders":
            session = get_session()
            orders = session.query(Order).all()
            self.table.setColumnCount(4)  # Adjust number of columns to match the data
            self.table.setHorizontalHeaderLabels(["Order ID", "Customer ID", "Total Amount", "Details"])

            for row_idx, order in enumerate(orders):
                self.table.insertRow(row_idx)
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(order.id)))  # Order ID
                self.table.setItem(row_idx, 1, QTableWidgetItem(str(order.customer_id)))  # Customer ID
                self.table.setItem(row_idx, 2, QTableWidgetItem(f"${order.total_amount}"))  # Total Amount

                # Fetch order items and construct the details string
                order_items = session.query(OrderItem).filter_by(order_id=order.id).all()
                details = ", ".join([f"{item.product.name} x {item.quantity}" for item in order_items])
                self.table.setItem(row_idx, 3, QTableWidgetItem(details))  # Order details

            session.close()  # Close the session when done






if __name__ == "__main__":
    app = QApplication([])
    main = mainClass()
    main.show()
    app.exec()

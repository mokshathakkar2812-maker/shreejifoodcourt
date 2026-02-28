import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class FoodApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shreeji Food Court")
        self.setGeometry(100, 100, 900, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        title = QLabel("🍽 Shreeji Food Court")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(title)

        # Category Buttons
        btn_layout = QHBoxLayout()

        self.fast_btn = QPushButton("Fast Food")
        self.indian_btn = QPushButton("Indian")
        self.dessert_btn = QPushButton("Desserts")
        self.snack_btn = QPushButton("Snacks")

        btn_layout.addWidget(self.fast_btn)
        btn_layout.addWidget(self.indian_btn)
        btn_layout.addWidget(self.dessert_btn)
        btn_layout.addWidget(self.snack_btn)

        self.layout.addLayout(btn_layout)

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.grid = QGridLayout()
        self.scroll_content.setLayout(self.grid)
        self.scroll.setWidget(self.scroll_content)

        self.layout.addWidget(self.scroll)

        # Bottom Buttons
        bottom_layout = QHBoxLayout()

        self.pay_btn = QPushButton("💳 Pay")
        self.rate_btn = QPushButton("⭐ Rate Us")
        self.admin_btn = QPushButton("🔐 Admin View")

        bottom_layout.addWidget(self.pay_btn)
        bottom_layout.addWidget(self.rate_btn)
        bottom_layout.addWidget(self.admin_btn)

        self.layout.addLayout(bottom_layout)

        # Button Connections
        self.fast_btn.clicked.connect(lambda: self.load_items("Fast Food"))
        self.indian_btn.clicked.connect(lambda: self.load_items("Indian"))
        self.dessert_btn.clicked.connect(lambda: self.load_items("Desserts"))
        self.snack_btn.clicked.connect(lambda: self.load_items("Snacks"))

        self.pay_btn.clicked.connect(self.pay_now)
        self.rate_btn.clicked.connect(self.rate_us)
        self.admin_btn.clicked.connect(self.admin_view)

        self.cart_total = 0

    def load_items(self, category):
        # Clear old items
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

        conn = sqlite3.connect("shreeji.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, image FROM menu WHERE category=?", (category,))
        items = cursor.fetchall()
        conn.close()

        row = 0
        col = 0

        for name, price, image in items:
            card = QVBoxLayout()

            img_label = QLabel()
            pixmap = QPixmap(image)
            pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)
            img_label.setPixmap(pixmap)

            name_label = QLabel(f"{name}\n₹{price}")
            name_label.setAlignment(Qt.AlignCenter)

            order_btn = QPushButton("Order")
            order_btn.clicked.connect(lambda _, n=name, p=price: self.place_order(n, p))

            card.addWidget(img_label)
            card.addWidget(name_label)
            card.addWidget(order_btn)

            container = QWidget()
            container.setLayout(card)

            self.grid.addWidget(container, row, col)

            col += 1
            if col == 3:
                col = 0
                row += 1

    def place_order(self, name, price):
        conn = sqlite3.connect("shreeji.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (item, price, status) VALUES (?, ?, ?)",
                       (name, price, "Pending"))
        conn.commit()
        conn.close()

        self.cart_total += price

        QMessageBox.information(self, "Order Placed", f"{name} added!\nTotal: ₹{self.cart_total}")

    def pay_now(self):
        if self.cart_total == 0:
            QMessageBox.warning(self, "Empty", "No items in cart!")
            return

        QMessageBox.information(self, "Payment Success", f"Paid ₹{self.cart_total} successfully!")
        self.cart_total = 0

    def rate_us(self):
        rating, ok = QInputDialog.getInt(self, "Rate Us", "Give rating (1-5):", 5, 1, 5)
        if ok:
            conn = sqlite3.connect("shreeji.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ratings (rating) VALUES (?)", (rating,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Thank You", "Thanks for rating us!")

    def admin_view(self):
        password, ok = QInputDialog.getText(self, "Admin Login", "Enter password:")
        if ok and password == "admin123":
            conn = sqlite3.connect("shreeji.db")
            cursor = conn.cursor()
            cursor.execute("SELECT item, price, status FROM orders")
            orders = cursor.fetchall()
            conn.close()

            message = ""
            total = 0
            for item, price, status in orders:
                message += f"{item} - ₹{price} - {status}\n"
                total += price

            message += f"\nTotal Sales: ₹{total}"

            QMessageBox.information(self, "Admin Orders", message)
        else:
            QMessageBox.warning(self, "Error", "Wrong Password!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FoodApp()
    window.show()
    sys.exit(app.exec_())
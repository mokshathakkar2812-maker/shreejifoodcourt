import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class CustomerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shreeji Food Court - Customer")
        self.setGeometry(100, 100, 900, 600)

        self.cart_total = 0

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        title = QLabel("🍽 Welcome to Shreeji Food Court")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        main_layout.addWidget(title)

        # Category buttons
        cat_layout = QHBoxLayout()

        categories = ["Fast Food", "Indian", "Desserts", "Snacks"]
        for cat in categories:
            btn = QPushButton(cat)
            btn.clicked.connect(lambda _, c=cat: self.load_items(c))
            cat_layout.addWidget(btn)

        main_layout.addLayout(cat_layout)

        # Scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.grid = QGridLayout()
        self.scroll_content.setLayout(self.grid)
        self.scroll.setWidget(self.scroll_content)

        main_layout.addWidget(self.scroll)

        # Bottom buttons
        bottom_layout = QHBoxLayout()

        pay_btn = QPushButton("💳 Pay")
        rate_btn = QPushButton("⭐ Rate Us")

        pay_btn.clicked.connect(self.pay_now)
        rate_btn.clicked.connect(self.rate_us)

        bottom_layout.addWidget(pay_btn)
        bottom_layout.addWidget(rate_btn)

        main_layout.addLayout(bottom_layout)

    def load_items(self, category):
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

        conn = sqlite3.connect("shreeji.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, image FROM menu WHERE category=?", (category,))
        items = cursor.fetchall()
        conn.close()

        row, col = 0, 0

        for name, price, image in items:
            layout = QVBoxLayout()

            img = QLabel()
            pixmap = QPixmap(image)
            pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)
            img.setPixmap(pixmap)

            label = QLabel(f"{name}\n₹{price}")
            label.setAlignment(Qt.AlignCenter)

            btn = QPushButton("Order")
            btn.clicked.connect(lambda _, n=name, p=price: self.place_order(n, p))

            layout.addWidget(img)
            layout.addWidget(label)
            layout.addWidget(btn)

            container = QWidget()
            container.setLayout(layout)

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
        QMessageBox.information(self, "Added", f"{name} added!\nTotal: ₹{self.cart_total}")

    def pay_now(self):
        if self.cart_total == 0:
            QMessageBox.warning(self, "Empty", "No items ordered!")
            return

        QMessageBox.information(self, "Success", f"Payment of ₹{self.cart_total} successful!")
        self.cart_total = 0

    def rate_us(self):
        rating, ok = QInputDialog.getInt(self, "Rate Us", "Rate 1-5:", 5, 1, 5)
        if ok:
            conn = sqlite3.connect("shreeji.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ratings (rating) VALUES (?)", (rating,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Thanks", "Thank you for rating!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomerApp()
    window.show()
    sys.exit(app.exec_())
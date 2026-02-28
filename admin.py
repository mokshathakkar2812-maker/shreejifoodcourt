import sys
import sqlite3
from PyQt5.QtWidgets import *


class AdminApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shreeji Food Court - Admin")
        self.setGeometry(200, 200, 500, 500)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.text = QTextEdit()
        self.text.setReadOnly(True)

        refresh_btn = QPushButton("🔄 Refresh Orders")
        refresh_btn.clicked.connect(self.load_orders)

        layout.addWidget(refresh_btn)
        layout.addWidget(self.text)

        self.load_orders()

    def load_orders(self):
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

        self.text.setText(message)


if __name__ == "__main__":
    password, ok = QInputDialog.getText(None, "Admin Login", "Enter Password:")
    if ok and password == "admin123":
        app = QApplication(sys.argv)
        window = AdminApp()
        window.show()
        sys.exit(app.exec_())
    else:
        QMessageBox.warning(None, "Error", "Wrong Password!")
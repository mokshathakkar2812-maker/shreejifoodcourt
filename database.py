import sqlite3

conn = sqlite3.connect("shreeji.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    price INTEGER,
    image TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT,
    price INTEGER,
    status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rating INTEGER
)
""")

items = [

# FAST FOOD
("Veg Pizza", "Fast Food", 120, "images/veg_pizza.jpg"),
("Cheese Pizza", "Fast Food", 150, "images/cheese_pizza.jpg"),
("Burger", "Fast Food", 80, "images/burger.jpg"),
("Fries", "Fast Food", 60, "images/fries.jpg"),
("Noodles", "Fast Food", 90, "images/noodles.jpg"),
("Manchurian", "Fast Food", 100, "images/manchurian.jpg"),
("Pasta", "Fast Food", 110, "images/pasta.jpg"),
("Sandwich", "Fast Food", 70, "images/sandwich.jpg"),

# INDIAN
("Paneer Butter Masala", "Indian", 180, "images/paneer.jpg"),
("Dal Fry", "Indian", 120, "images/dalfry.jpg"),
("Veg Thali", "Indian", 200, "images/thali.jpg"),
("Chole Bhature", "Indian", 130, "images/chole.jpg"),
("Pav Bhaji", "Indian", 90, "images/pavbhaji.jpg"),
("Jeera Rice", "Indian", 100, "images/jeerarice.jpg"),
("Butter Roti", "Indian", 20, "images/roti.jpg"),
("Masala Dosa", "Indian", 110, "images/dosa.jpg"),

# DESSERTS
("Gulab Jamun", "Desserts", 60, "images/gulabjamun.jpg"),
("Ice Cream", "Desserts", 50, "images/icecream.jpg"),
("Brownie", "Desserts", 80, "images/brownie.jpg"),
("Cake", "Desserts", 90, "images/cake.jpg"),
("Rasmalai", "Desserts", 70, "images/rasmalai.jpg"),

# SNACKS
("Samosa", "Snacks", 20, "images/samosa.jpg"),
("Kachori", "Snacks", 25, "images/kachori.jpg"),
("Vadapav", "Snacks", 30, "images/vadapav.jpg"),
("Bhel Puri", "Snacks", 40, "images/bhelpuri.jpg"),
("Dhokla", "Snacks", 35, "images/dhokla.jpg"),
("Gota", "Snacks", 30, "images/gota.jpg"),
("Fafda", "Snacks", 40, "images/fafda.jpg"),
("Bread Pakora", "Snacks", 30, "images/breadpakora.jpg"),
]

cursor.executemany("INSERT INTO menu (name, category, price, image) VALUES (?, ?, ?, ?)", items)
conn.commit()
conn.close()

print("Database Created Successfully!")
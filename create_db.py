import sqlite3

# Connect to database (creates file if not exists)
conn = sqlite3.connect('vending.db')
c = conn.cursor()

# Create products table
c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL
    )
''')

# Seed products
products = [
    ('Chocolate Bar', 'Delicious milk chocolate.', 1.50),
    ('Bottle of Water', '500ml mineral water.', 1.00),
    ('Packet of Crisps', 'Salted potato chips.', 1.25),
]

# Insert products
c.executemany('INSERT INTO products (name, description, price) VALUES (?, ?, ?)', products)

# Commit and close
conn.commit()
conn.close()

print("Database created and seeded!")

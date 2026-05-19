import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "inventory.db")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS inventory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def check_data():
    conn = sqlite3.connect(DB_NAME)
    cr = conn.cursor()
    cr.execute('SELECT * FROM inventory')
    print("Current Inventory Data:", cr.fetchall())
    conn.close()
    
# Function to get all inventory items
def get_all_items():
    conn = sqlite3.connect(DB_NAME)
    cr = conn.cursor()
    cr.execute('SELECT * FROM inventory')
    items = cr.fetchall()
    conn.close()
    return items

# Function to add a new inventory item to the table
def add_item(name, quantity, price):
    conn = sqlite3.connect(DB_NAME)
    cr = conn.cursor()
    # Removed the redundant 'SELECT *' line that wasn't being used
    cr.execute('INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))
    conn.commit()
    conn.close()
    
# Function to Delete an Item
def delete_item(item_id):
    conn = sqlite3.connect(DB_NAME)
    cr = conn.cursor()
    cr.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

# Function to get Item based on ID
def get_item_by_id(item_id):
    conn = sqlite3.connect(DB_NAME)
    cr = conn.cursor()
    cr.execute('SELECT * FROM inventory WHERE id = ?', (item_id,))
    item = cr.fetchone()
    conn.close()
    return item

# Function to update Item Based on ID
def update_item(item_id, name, quantity, price):
    conn = sqlite3.connect(DB_NAME)
    cr = conn.cursor()
    cr.execute('UPDATE inventory SET name = ?, quantity = ?, price = ? WHERE id = ?', (name, quantity, price, item_id))
    conn.commit()
    conn.close() 
    
if __name__ == "__main__":
    init_db()
    print("Adding a test item...")
    check_data()
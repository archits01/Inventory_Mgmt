from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
import json
import heapq
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

DATABASE = 'inventory.db'

class InventoryManager:
    def __init__(self):
        self.items = {}
        self.low_stock_heap = []
        self.threshold = 10
        self.init_db()
        self.load_items()
    
    def init_db(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        cursor.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', 
                      ('low_stock_threshold', '10'))
        conn.commit()
        conn.close()
    
    def load_items(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT name, quantity, price FROM items')
        items = cursor.fetchall()
        
        cursor.execute('SELECT value FROM settings WHERE key = ?', ('low_stock_threshold',))
        threshold_row = cursor.fetchone()
        if threshold_row:
            self.threshold = int(threshold_row[0])
        
        conn.close()
        
        self.items = {}
        self.low_stock_heap = []
        
        for name, quantity, price in items:
            self.items[name] = {
                'quantity': quantity,
                'price': price
            }
            if quantity < self.threshold:
                heapq.heappush(self.low_stock_heap, (quantity, name))
    
    def add_item(self, name, quantity, price):
        if name in self.items:
            return False, "Item already exists"
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)',
                         (name, quantity, price))
            conn.commit()
            conn.close()
            
            self.items[name] = {
                'quantity': quantity,
                'price': price
            }
            
            if quantity < self.threshold:
                heapq.heappush(self.low_stock_heap, (quantity, name))
            
            return True, "Item added successfully"
        except sqlite3.IntegrityError:
            conn.close()
            return False, "Item already exists"
    
    def update_item(self, name, quantity=None, price=None):
        if name not in self.items:
            return False, "Item not found"
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        if quantity is not None:
            self.items[name]['quantity'] = quantity
            cursor.execute('UPDATE items SET quantity = ?, updated_at = CURRENT_TIMESTAMP WHERE name = ?',
                         (quantity, name))
        
        if price is not None:
            self.items[name]['price'] = price
            cursor.execute('UPDATE items SET price = ?, updated_at = CURRENT_TIMESTAMP WHERE name = ?',
                         (price, name))
        
        conn.commit()
        conn.close()
        
        self._rebuild_heap()
        
        return True, "Item updated successfully"
    
    def delete_item(self, name):
        if name not in self.items:
            return False, "Item not found"
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items WHERE name = ?', (name,))
        conn.commit()
        conn.close()
        
        del self.items[name]
        self._rebuild_heap()
        
        return True, "Item deleted successfully"
    
    def get_all_items(self):
        items_list = []
        for name, data in self.items.items():
            items_list.append({
                'name': name,
                'quantity': data['quantity'],
                'price': data['price']
            })
        return items_list
    
    def get_low_stock_items(self):
        low_stock = []
        temp_heap = []
        
        while self.low_stock_heap:
            quantity, name = heapq.heappop(self.low_stock_heap)
            if name in self.items and self.items[name]['quantity'] < self.threshold:
                low_stock.append({
                    'name': name,
                    'quantity': self.items[name]['quantity'],
                    'price': self.items[name]['price']
                })
                temp_heap.append((self.items[name]['quantity'], name))
        
        self.low_stock_heap = temp_heap
        heapq.heapify(self.low_stock_heap)
        
        return low_stock
    
    def search_items(self, query):
        results = []
        query_lower = query.lower()
        for name, data in self.items.items():
            if query_lower in name.lower():
                results.append({
                    'name': name,
                    'quantity': data['quantity'],
                    'price': data['price']
                })
        return results
    
    def set_threshold(self, threshold):
        self.threshold = threshold
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('UPDATE settings SET value = ? WHERE key = ?',
                      (str(threshold), 'low_stock_threshold'))
        conn.commit()
        conn.close()
        self._rebuild_heap()
    
    def _rebuild_heap(self):
        self.low_stock_heap = []
        for name, data in self.items.items():
            if data['quantity'] < self.threshold:
                heapq.heappush(self.low_stock_heap, (data['quantity'], name))

inventory = InventoryManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(inventory.get_all_items())

@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.json
    success, message = inventory.add_item(
        data['name'],
        int(data['quantity']),
        float(data['price'])
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/items/<name>', methods=['PUT'])
def update_item(name):
    data = request.json
    quantity = int(data['quantity']) if 'quantity' in data else None
    price = float(data['price']) if 'price' in data else None
    success, message = inventory.update_item(name, quantity, price)
    return jsonify({'success': success, 'message': message})

@app.route('/api/items/<name>', methods=['DELETE'])
def delete_item(name):
    success, message = inventory.delete_item(name)
    return jsonify({'success': success, 'message': message})

@app.route('/api/low-stock', methods=['GET'])
def get_low_stock():
    return jsonify(inventory.get_low_stock_items())

@app.route('/api/search', methods=['GET'])
def search_items():
    query = request.args.get('q', '')
    return jsonify(inventory.search_items(query))

@app.route('/api/threshold', methods=['GET'])
def get_threshold():
    return jsonify({'threshold': inventory.threshold})

@app.route('/api/threshold', methods=['POST'])
def set_threshold():
    data = request.json
    inventory.set_threshold(int(data['threshold']))
    return jsonify({'success': True, 'message': 'Threshold updated'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
# Inventory Management System

A web-based inventory management system demonstrating the use of hashmaps (dictionaries) and priority queues (min-heap) for efficient data organization.

## Features

- **Add, Update, Delete Items**: Manage inventory items with name, quantity, and price
- **Fast Lookup**: Uses Python dictionary (hashmap) for O(1) item retrieval
- **Low Stock Alerts**: Automatic tracking using a min-heap priority queue
- **Search Functionality**: Search items by name
- **Sortable Inventory**: Sort by name, quantity, or price
- **Customizable Threshold**: Set your own low stock threshold
- **Persistent Storage**: SQLite database stored locally in `inventory.db`

## Data Structures Used

1. **HashMap (Dictionary)**: 
   - Python `dict` for O(1) item lookup by name
   - Efficient storage and retrieval of inventory items

2. **Priority Queue (Min-Heap)**:
   - Python `heapq` for tracking low stock items
   - Automatically maintains items sorted by quantity
   - Efficient O(log n) updates when quantities change

## Installation & Running

1. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   ./run.sh
   # Or directly: python3 app.py
   ```

3. Open your browser to: http://localhost:5000

## Usage

1. **Add Items**: Use the form at the top to add new inventory items
2. **Update Items**: Click "Edit" on any item to modify quantity or price
3. **Delete Items**: Click "Delete" to remove items from inventory
4. **Search**: Use the search box to find items by name
5. **Sort**: Use the dropdown to sort items by different criteria
6. **Low Stock**: Items below the threshold appear in the Low Stock section
7. **Adjust Threshold**: Change the low stock threshold value as needed

## Technical Details

- **Backend**: Flask (Python) REST API
- **Frontend**: Vanilla JavaScript with dynamic updates
- **Database**: SQLite with local storage
- **Architecture**: MVC pattern with clean separation of concerns
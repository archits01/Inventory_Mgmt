# Inventory Management System - Technical Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Database Design](#database-design)
5. [Backend Implementation](#backend-implementation)
6. [Frontend Implementation](#frontend-implementation)
7. [API Documentation](#api-documentation)
8. [Data Structures](#data-structures)
9. [Security Considerations](#security-considerations)
10. [Deployment and Configuration](#deployment-and-configuration)
11. [File-by-File Breakdown](#file-by-file-breakdown)
12. [Future Enhancements](#future-enhancements)

## Project Overview

This inventory management system is a full-stack web application built with Flask (Python) backend and vanilla JavaScript frontend. It demonstrates the practical implementation of fundamental data structures (HashMap and Priority Queue) in a real-world application context.

### Key Features
- **CRUD Operations**: Complete inventory management (Create, Read, Update, Delete)
- **Real-time Search**: Instant item search functionality
- **Low Stock Tracking**: Automatic monitoring using priority queue (min-heap)
- **Responsive Design**: Mobile-friendly interface
- **Persistent Storage**: SQLite database with automatic initialization
- **Sorting Capabilities**: Sort by name, quantity, or price

## Architecture

### System Architecture
```
┌─────────────────────────────────────────────────────────┐
│                   Client (Browser)                      │
│  ┌─────────────────────────────────────────────────┐  │
│  │              Frontend (HTML/CSS/JS)              │  │
│  │  ├── index.html (Structure)                     │  │
│  │  ├── style.css (Presentation)                   │  │
│  │  └── script.js (Behavior)                       │  │
│  └─────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────┘
                     │ HTTP/AJAX (JSON)
┌────────────────────┴───────────────────────────────────┐
│                   Server (Flask)                        │
│  ┌─────────────────────────────────────────────────┐  │
│  │                  app.py                          │  │
│  │  ├── Route Handlers                             │  │
│  │  ├── Business Logic                             │  │
│  │  ├── Data Structures (HashMap, Priority Queue)  │  │
│  │  └── Database Interface                         │  │
│  └─────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────┘
                     │ SQL
┌────────────────────┴───────────────────────────────────┐
│                Database (SQLite)                        │
│  ┌─────────────────────────────────────────────────┐  │
│  │              inventory.db                        │  │
│  │  ├── items table                                │  │
│  │  └── settings table                             │  │
│  └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Directory Structure
```
Inventory_mgmt/
├── app.py                    # Backend Flask application
├── inventory.db              # SQLite database file
├── requirements.txt          # Python dependencies
├── run.sh                    # Startup script
├── static/                   # Frontend assets
│   ├── script.js            # Client-side JavaScript
│   └── style.css            # Styling
├── templates/               # Flask templates
│   └── index.html           # Main HTML page
└── venv/                    # Python virtual environment
```

## Technology Stack

### Backend Technologies
- **Flask 3.0.0**: Lightweight Python web framework
  - Chosen for simplicity and educational purposes
  - Provides routing, request handling, and templating
- **Flask-CORS 4.0.0**: Cross-Origin Resource Sharing support
  - Enables API access from different origins
- **SQLite 3.x**: Embedded relational database
  - Zero-configuration database
  - Perfect for small to medium applications
- **Python 3.13.6**: Latest Python version
  - Modern language features
  - Type hints support

### Frontend Technologies
- **HTML5**: Semantic markup with modern features
- **CSS3**: Modern styling with Grid and Flexbox
- **JavaScript (ES6+)**: Vanilla JS with async/await
- **Fetch API**: Modern AJAX requests

### Development Tools
- **Virtual Environment**: Python venv for dependency isolation
- **Shell Script**: Automated startup script

## Database Design

### Schema Definition

#### Items Table
```sql
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields Explanation:**
- `id`: Auto-incrementing primary key for unique identification
- `name`: Unique constraint ensures no duplicate items
- `quantity`: Integer value for stock count
- `price`: Real number for item pricing
- `created_at`: Automatic timestamp on record creation
- `updated_at`: Timestamp for tracking modifications

#### Settings Table
```sql
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

**Purpose**: Key-value store for application configuration
- Currently stores `low_stock_threshold` (default: 10)

### Database Initialization
The database is automatically created and initialized on first run:
1. Creates tables if they don't exist
2. Sets default low stock threshold to 10
3. Uses SQLite's built-in transaction support

## Backend Implementation

### Core Components in app.py

#### 1. Data Structure Implementation

**HashMap (items_map)**
```python
items_map = {}  # O(1) lookup by item name
```
- Maps item names to their database records
- Provides constant-time lookup for validation and retrieval
- Updated on every CRUD operation

**Priority Queue (low_stock_heap)**
```python
low_stock_heap = []  # Min-heap for low stock tracking
```
- Maintains items with quantity below threshold
- Uses Python's heapq module
- Tuple format: `(quantity, name)`
- Automatically updated on item changes

#### 2. Database Helper Functions

**get_db_connection()**
- Creates and returns SQLite connection
- Enables row factory for dict-like access
- Handles connection lifecycle

**init_db()**
- Creates tables on first run
- Sets default configuration
- Idempotent operation

#### 3. Core Business Logic

**update_data_structures()**
- Rebuilds HashMap from database
- Reconstructs priority queue for low stock items
- Called after any data modification
- Ensures data consistency

### Route Handlers

#### Static Routes
- `GET /`: Serves the main web interface (index.html)

#### API Routes
All API routes return JSON responses with consistent structure:
```json
{
    "success": true/false,
    "message": "Operation result",
    "data": {} // Optional data payload
}
```

## Frontend Implementation

### HTML Structure (index.html)

#### Key Sections:
1. **Header**
   - Application title
   - Search input with real-time filtering
   - Low stock threshold control

2. **Add Item Form**
   - Input fields for name, quantity, price
   - Client-side validation
   - Submit button

3. **All Items Table**
   - Sortable columns (name, quantity, price)
   - Edit and delete actions per row
   - Dynamic content generation

4. **Low Stock Section**
   - Displays items below threshold
   - Auto-updates on changes

5. **Edit Modal**
   - Popup for editing existing items
   - Pre-populated with current values

### JavaScript Implementation (script.js)

#### State Management
```javascript
let allItems = [];          // Local cache of all items
let currentSort = null;     // Current sort configuration
```

#### Core Functions:

**fetchItems()**
- Retrieves all items from backend
- Updates local state
- Triggers UI refresh

**renderItems(items)**
- Generates HTML for items table
- Applies current sorting
- Handles empty state

**renderLowStock()**
- Fetches and displays low stock items
- Shows/hides based on content

**Event Handlers**
- Form submissions (add/edit)
- Modal interactions
- Sort column clicks
- Search input changes
- Threshold updates

### CSS Styling (style.css)

#### Design Philosophy:
- **Mobile-First**: Responsive breakpoints
- **Modern Layout**: CSS Grid and Flexbox
- **Clean UI**: Minimalist design with good contrast
- **Accessibility**: Proper focus states and hover effects

#### Key Styles:
1. **Container**: Max-width 1200px, centered
2. **Grid Layouts**: Forms and header sections
3. **Table Styling**: Responsive with horizontal scroll
4. **Modal**: Overlay with centered content
5. **Button States**: Hover and active effects
6. **Color Scheme**: Blue primary (#007bff), danger red (#dc3545)

## API Documentation

### Endpoints

#### 1. GET /api/items
**Description**: Retrieve all inventory items
**Response**:
```json
[
    {
        "id": 1,
        "name": "Item Name",
        "quantity": 50,
        "price": 29.99,
        "created_at": "2024-01-01 12:00:00",
        "updated_at": "2024-01-01 12:00:00"
    }
]
```

#### 2. POST /api/items
**Description**: Add new inventory item
**Request Body**:
```json
{
    "name": "New Item",
    "quantity": 100,
    "price": 19.99
}
```
**Validation**:
- Name: Required, unique, non-empty
- Quantity: Required, non-negative integer
- Price: Required, non-negative number

#### 3. PUT /api/items/<name>
**Description**: Update existing item
**URL Parameter**: Item name (URL encoded)
**Request Body**:
```json
{
    "quantity": 150,
    "price": 24.99
}
```
**Notes**: Name cannot be changed (used as identifier)

#### 4. DELETE /api/items/<name>
**Description**: Remove item from inventory
**URL Parameter**: Item name (URL encoded)

#### 5. GET /api/low-stock
**Description**: Get items below threshold
**Response**: Array of items with quantity < threshold

#### 6. GET /api/search?q=<query>
**Description**: Search items by name
**Query Parameter**: q (search term)
**Behavior**: Case-insensitive partial match

#### 7. GET /api/threshold
**Description**: Get current low stock threshold
**Response**:
```json
{
    "threshold": 10
}
```

#### 8. POST /api/threshold
**Description**: Update low stock threshold
**Request Body**:
```json
{
    "threshold": 15
}
```

## Data Structures

### HashMap Implementation

**Purpose**: O(1) item lookup by name
**Structure**:
```python
items_map = {
    "item_name": {
        "id": 1,
        "name": "item_name",
        "quantity": 50,
        "price": 29.99,
        "created_at": "...",
        "updated_at": "..."
    }
}
```

**Operations**:
- **Insert**: O(1) - Direct key assignment
- **Lookup**: O(1) - Direct key access
- **Delete**: O(1) - Direct key removal
- **Update**: O(1) - Direct key access and modification

### Priority Queue Implementation

**Purpose**: Efficient tracking of low stock items
**Structure**: Min-heap using Python's heapq
```python
low_stock_heap = [
    (5, "Item A"),    # (quantity, name)
    (7, "Item B"),
    (9, "Item C")
]
```

**Operations**:
- **Insert**: O(log n) - heappush
- **Extract Min**: O(log n) - heappop
- **Peek Min**: O(1) - heap[0]
- **Build Heap**: O(n) - heapify

**Algorithm**: Maintains heap property where parent quantity ≤ children quantities

## Security Considerations

### Current Security Measures

1. **SQL Injection Prevention**
   - Parameterized queries using `?` placeholders
   - SQLite's built-in escaping

2. **Input Validation**
   - Server-side validation for all inputs
   - Type checking and range validation
   - Unique constraint enforcement

3. **XSS Prevention**
   - No direct HTML injection
   - JSON responses only
   - Client-side text content setting

### Security Vulnerabilities

1. **No Authentication**
   - Anyone can access the system
   - No user accounts or sessions

2. **No Authorization**
   - No role-based access control
   - All users have full CRUD permissions

3. **No Rate Limiting**
   - Potential for DoS attacks
   - No request throttling

4. **Debug Mode**
   - Flask debug mode enabled
   - Should be disabled in production

5. **No HTTPS**
   - Data transmitted in plain text
   - No encryption

### Recommended Security Enhancements

1. Implement user authentication (Flask-Login)
2. Add role-based authorization
3. Enable HTTPS with SSL certificates
4. Implement rate limiting (Flask-Limiter)
5. Add CSRF protection
6. Disable debug mode in production
7. Add input sanitization
8. Implement audit logging

## Deployment and Configuration

### Development Setup

1. **Clone Repository**
```bash
git clone [repository-url]
cd Inventory_mgmt
```

2. **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Application**
```bash
./run.sh
# or
python3 app.py
```

5. **Access Application**
- Open browser to `http://localhost:5000`

### Configuration Files

#### requirements.txt
```
Flask==3.0.0
Flask-CORS==4.0.0
```
- Minimal dependencies
- Exact version pinning for reproducibility

#### run.sh
```bash
#!/bin/bash
if [ -d "venv" ]; then
    source venv/bin/activate
fi
python3 app.py
```
- Automatic venv activation
- Cross-platform Python 3 execution

### Production Deployment Considerations

1. **Web Server**
   - Use Gunicorn or uWSGI instead of Flask's built-in server
   - Configure worker processes

2. **Reverse Proxy**
   - Set up Nginx or Apache
   - Handle SSL termination
   - Serve static files directly

3. **Database**
   - Consider PostgreSQL or MySQL for production
   - Implement connection pooling
   - Set up regular backups

4. **Environment Variables**
   - Move configuration to environment
   - Use python-dotenv for .env files

5. **Monitoring**
   - Add application logging
   - Implement error tracking (Sentry)
   - Set up performance monitoring

## File-by-File Breakdown

### app.py (340 lines)
**Purpose**: Backend server implementation
**Key Sections**:
- Lines 1-10: Import statements
- Lines 12-25: Global data structures
- Lines 27-75: Database initialization
- Lines 77-120: Data structure update logic
- Lines 122-340: Route handlers

### static/script.js (285 lines)
**Purpose**: Frontend interactivity
**Key Sections**:
- Lines 1-15: Global state variables
- Lines 17-50: Item fetching and rendering
- Lines 52-120: Low stock management
- Lines 122-200: Form handling
- Lines 202-285: Event listeners and utilities

### static/style.css (180 lines)
**Purpose**: Visual styling
**Key Sections**:
- Lines 1-30: Base styles and variables
- Lines 32-80: Layout containers
- Lines 82-130: Form and input styles
- Lines 132-180: Table and responsive design

### templates/index.html (95 lines)
**Purpose**: HTML structure
**Key Components**:
- DOCTYPE and meta tags
- Header section with controls
- Add item form
- Items table container
- Low stock section
- Edit modal

## Future Enhancements

### Feature Enhancements
1. **Barcode Scanning**: Integrate barcode reader support
2. **Categories**: Add item categorization
3. **Suppliers**: Track supplier information
4. **Purchase Orders**: Automated reordering
5. **Reports**: Generate inventory reports
6. **Export/Import**: CSV/Excel support
7. **Images**: Product image uploads
8. **History**: Track all changes with audit trail

### Technical Improvements
1. **API Versioning**: Implement /api/v1/ structure
2. **Pagination**: Handle large datasets
3. **Caching**: Implement Redis caching
4. **WebSockets**: Real-time updates
5. **Testing**: Add unit and integration tests
6. **Documentation**: API documentation with Swagger
7. **Containerization**: Docker support
8. **CI/CD**: Automated testing and deployment

### Performance Optimizations
1. **Database Indexing**: Add indexes for search
2. **Lazy Loading**: Load data on demand
3. **Compression**: Enable gzip compression
4. **CDN**: Serve static assets via CDN
5. **Connection Pooling**: Database connection reuse
6. **Query Optimization**: Analyze and optimize SQL

This inventory management system serves as an excellent educational project demonstrating full-stack development, data structure implementation, and modern web technologies. The clean architecture and comprehensive features make it a solid foundation for learning and potential expansion into a production-ready application.
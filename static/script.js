let allItems = [];
let currentSort = 'name';

async function loadItems() {
    try {
        const response = await fetch('/api/items');
        allItems = await response.json();
        displayItems();
        loadLowStockItems();
    } catch (error) {
        console.error('Error loading items:', error);
    }
}

async function loadLowStockItems() {
    try {
        const response = await fetch('/api/low-stock');
        const lowStockItems = await response.json();
        displayLowStockItems(lowStockItems);
    } catch (error) {
        console.error('Error loading low stock items:', error);
    }
}

async function loadThreshold() {
    try {
        const response = await fetch('/api/threshold');
        const data = await response.json();
        document.getElementById('thresholdInput').value = data.threshold;
    } catch (error) {
        console.error('Error loading threshold:', error);
    }
}

function displayItems() {
    const itemsTable = document.getElementById('itemsTable');
    
    if (allItems.length === 0) {
        itemsTable.innerHTML = '<div class="no-items">No items in inventory</div>';
        return;
    }
    
    sortItemsArray();
    
    let html = `
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Quantity</th>
                    <th>Price</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    allItems.forEach(item => {
        const quantityClass = item.quantity < 10 ? 'low-quantity' : '';
        html += `
            <tr>
                <td>${item.name}</td>
                <td class="${quantityClass}">${item.quantity}</td>
                <td>$${item.price.toFixed(2)}</td>
                <td class="actions">
                    <button class="edit-btn" onclick="openEditModal('${item.name}', ${item.quantity}, ${item.price})">Edit</button>
                    <button class="delete-btn" onclick="deleteItem('${item.name}')">Delete</button>
                </td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    itemsTable.innerHTML = html;
}

function displayLowStockItems(items) {
    const lowStockTable = document.getElementById('lowStockTable');
    
    if (items.length === 0) {
        lowStockTable.innerHTML = '<div class="no-items">No low stock items</div>';
        return;
    }
    
    let html = `
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Quantity</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    items.forEach(item => {
        html += `
            <tr>
                <td>${item.name}</td>
                <td class="low-quantity">${item.quantity}</td>
                <td>$${item.price.toFixed(2)}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    lowStockTable.innerHTML = html;
}

function sortItemsArray() {
    switch (currentSort) {
        case 'name':
            allItems.sort((a, b) => a.name.localeCompare(b.name));
            break;
        case 'quantity':
            allItems.sort((a, b) => a.quantity - b.quantity);
            break;
        case 'price':
            allItems.sort((a, b) => a.price - b.price);
            break;
    }
}

function sortItems() {
    currentSort = document.getElementById('sortSelect').value;
    displayItems();
}

async function addItem(event) {
    event.preventDefault();
    
    const name = document.getElementById('itemName').value;
    const quantity = parseInt(document.getElementById('itemQuantity').value);
    const price = parseFloat(document.getElementById('itemPrice').value);
    
    try {
        const response = await fetch('/api/items', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, quantity, price }),
        });
        
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('addItemForm').reset();
            await loadItems();
        } else {
            alert(result.message);
        }
    } catch (error) {
        console.error('Error adding item:', error);
        alert('Error adding item');
    }
}

function openEditModal(name, quantity, price) {
    document.getElementById('editItemName').value = name;
    document.getElementById('editItemNameDisplay').textContent = name;
    document.getElementById('editItemQuantity').value = quantity;
    document.getElementById('editItemPrice').value = price;
    document.getElementById('editModal').style.display = 'block';
}

function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

async function updateItem(event) {
    event.preventDefault();
    
    const name = document.getElementById('editItemName').value;
    const quantity = parseInt(document.getElementById('editItemQuantity').value);
    const price = parseFloat(document.getElementById('editItemPrice').value);
    
    try {
        const response = await fetch(`/api/items/${encodeURIComponent(name)}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ quantity, price }),
        });
        
        const result = await response.json();
        
        if (result.success) {
            closeEditModal();
            await loadItems();
        } else {
            alert(result.message);
        }
    } catch (error) {
        console.error('Error updating item:', error);
        alert('Error updating item');
    }
}

async function deleteItem(name) {
    if (!confirm(`Are you sure you want to delete "${name}"?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/items/${encodeURIComponent(name)}`, {
            method: 'DELETE',
        });
        
        const result = await response.json();
        
        if (result.success) {
            await loadItems();
        } else {
            alert(result.message);
        }
    } catch (error) {
        console.error('Error deleting item:', error);
        alert('Error deleting item');
    }
}

async function searchItems() {
    const query = document.getElementById('searchInput').value;
    
    if (!query) {
        await loadItems();
        return;
    }
    
    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        allItems = await response.json();
        displayItems();
    } catch (error) {
        console.error('Error searching items:', error);
    }
}

async function updateThreshold() {
    const threshold = parseInt(document.getElementById('thresholdInput').value);
    
    if (threshold < 1) {
        alert('Threshold must be at least 1');
        return;
    }
    
    try {
        const response = await fetch('/api/threshold', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ threshold }),
        });
        
        const result = await response.json();
        
        if (result.success) {
            await loadLowStockItems();
            alert('Threshold updated successfully');
        }
    } catch (error) {
        console.error('Error updating threshold:', error);
        alert('Error updating threshold');
    }
}

window.onclick = function(event) {
    if (event.target == document.getElementById('editModal')) {
        closeEditModal();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    loadItems();
    loadThreshold();
});
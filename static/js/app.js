// IP Management Tool - Web Version - Frontend JavaScript

// State
let records = [];
let deletedRecords = [];
let editingIp = null;
let selectedRows = new Set();
let currentSort = { column: 'ip', reverse: false };

// ━━ INITIALIZATION ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

document.addEventListener('DOMContentLoaded', () => {
    // Load initial data
    loadRecords();
    updateSummary();
    
    // Event listeners - Search and Buttons
    document.getElementById('searchInput').addEventListener('keyup', () => {
        loadRecords();
    });
    
    document.getElementById('selectAll').addEventListener('change', (e) => {
        selectAllRows(e.target.checked);
    });
    
    document.getElementById('btnAdd').addEventListener('click', () => openAddDialog());
    document.getElementById('btnEdit').addEventListener('click', () => openEditDialog());
    document.getElementById('btnDelete').addEventListener('click', () => deleteSelected());
    document.getElementById('btnImport').addEventListener('click', () => openImportDialog());
    document.getElementById('btnExport').addEventListener('click', () => exportRecords());
    document.getElementById('btnRecover').addEventListener('click', () => openRecoveryDialog());
    document.getElementById('btnRefresh').addEventListener('click', () => {
        loadRecords();
        updateSummary();
        showToast('Data refreshed', 'success');
    });
    document.getElementById('btnSettings').addEventListener('click', () => openSettingsDialog());
    
    // Form submission
    document.getElementById('recordForm').addEventListener('submit', (e) => {
        e.preventDefault();
        saveRecord();
    });
    
    // Sort headers
    document.querySelectorAll('.records-table th.sortable').forEach(header => {
        header.addEventListener('click', () => {
            const column = header.dataset.column;
            if (currentSort.column === column) {
                currentSort.reverse = !currentSort.reverse;
            } else {
                currentSort.column = column;
                currentSort.reverse = false;
            }
            loadRecords();
        });
    });
});

// ━━ LOAD RECORDS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async function loadRecords() {
    try {
        const search = document.getElementById('searchInput').value;
        const url = `/api/records?search=${encodeURIComponent(search)}&sort_by=${currentSort.column}&sort_rev=${currentSort.reverse}`;
        
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to load records');
        
        const data = await response.json();
        records = data.data || [];
        
        renderTable();
        updateSummary();
    } catch (error) {
        console.error('Error loading records:', error);
        showToast('Error loading records', 'error');
    }
}

// ━━ RENDER TABLE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function renderTable() {
    const tbody = document.getElementById('tableBody');
    const emptyState = document.getElementById('emptyState');
    
    if (records.length === 0) {
        tbody.innerHTML = '';
        tbody.closest('.table-wrapper').style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }
    
    tbody.closest('.table-wrapper').style.display = 'block';
    emptyState.style.display = 'none';
    
    tbody.innerHTML = records.map(record => {
        const statusClass = `status-${record.status}`;
        const isSelected = selectedRows.has(record.ip);
        const selectedClass = isSelected ? 'selected' : '';
        const timestamp = new Date(record.timestamp).toLocaleDateString();
        
        return `
            <tr class="${selectedClass}" data-ip="${record.ip}">
                <td>
                    <input type="checkbox" class="checkbox row-checkbox" 
                           data-ip="${record.ip}" 
                           ${isSelected ? 'checked' : ''}>
                </td>
                <td><code>${record.ip}</code></td>
                <td>${record.hostname}</td>
                <td><span class="status-badge ${statusClass}">${record.status}</span></td>
                <td>${record.notes || '-'}</td>
                <td>${timestamp}</td>
            </tr>
        `;
    }).join('');
    
    // Add checkbox event listeners
    document.querySelectorAll('.row-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            const ip = e.target.dataset.ip;
            if (e.target.checked) {
                selectedRows.add(ip);
            } else {
                selectedRows.delete(ip);
                document.getElementById('selectAll').checked = false;
            }
            updateRowSelection();
        });
    });
    
    // Add row click listeners
    document.querySelectorAll('#tableBody tr').forEach(row => {
        row.addEventListener('click', (e) => {
            if (e.target.tagName === 'INPUT') return;
            const ip = row.dataset.ip;
            const checkbox = row.querySelector('.row-checkbox');
            checkbox.checked = !checkbox.checked;
            checkbox.dispatchEvent(new Event('change'));
        });
    });
}

function updateRowSelection() {
    document.querySelectorAll('#tableBody tr').forEach(row => {
        const ip = row.dataset.ip;
        if (selectedRows.has(ip)) {
            row.classList.add('selected');
        } else {
            row.classList.remove('selected');
        }
    });
}

function selectAllRows(select) {
    if (select) {
        records.forEach(r => selectedRows.add(r.ip));
    } else {
        selectedRows.clear();
    }
    updateRowSelection();
    document.querySelectorAll('.row-checkbox').forEach(cb => {
        cb.checked = select;
    });
}

// ━━ CRUD OPERATIONS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function openAddDialog() {
    editingIp = null;
    document.getElementById('dialogTitle').textContent = 'Add IP Record';
    document.getElementById('recordForm').reset();
    document.getElementById('ipInput').disabled = false;
    openDialog('recordDialog');
}

function openEditDialog() {
    if (selectedRows.size === 0) {
        showToast('Select a record to edit', 'warning');
        return;
    }
    if (selectedRows.size > 1) {
        showToast('Select only one record to edit', 'warning');
        return;
    }
    
    editingIp = Array.from(selectedRows)[0];
    const record = records.find(r => r.ip === editingIp);
    
    if (!record) return;
    
    document.getElementById('dialogTitle').textContent = 'Edit IP Record';
    document.getElementById('ipInput').value = record.ip;
    document.getElementById('ipInput').disabled = true;
    document.getElementById('hostnameInput').value = record.hostname;
    document.getElementById('statusSelect').value = record.status;
    document.getElementById('notesInput').value = record.notes || '';
    
    openDialog('recordDialog');
}

async function saveRecord() {
    const ip = document.getElementById('ipInput').value.trim();
    const hostname = document.getElementById('hostnameInput').value.trim();
    const status = document.getElementById('statusSelect').value;
    const notes = document.getElementById('notesInput').value.trim();
    
    // Validate
    if (!ip || !hostname || !status) {
        showToast('All fields are required', 'error');
        return;
    }
    
    if (!isValidIP(ip)) {
        document.getElementById('ipError').textContent = 'Invalid IP address format';
        return;
    }
    
    try {
        const endpoint = editingIp ? '/api/records/update' : '/api/records/add';
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ip, hostname, status, notes })
        });
        
        const data = await response.json();
        
        if (!data.success) {
            showToast(data.error || 'Failed to save record', 'error');
            return;
        }
        
        showToast(editingIp ? 'Record updated' : 'Record added', 'success');
        closeDialog('recordDialog');
        selectedRows.clear();
        loadRecords();
    } catch (error) {
        console.error('Error saving record:', error);
        showToast('Failed to save record', 'error');
    }
}

async function deleteSelected() {
    if (selectedRows.size === 0) {
        showToast('Select records to delete', 'warning');
        return;
    }
    
    if (!confirm(`Delete ${selectedRows.size} record(s)?`)) return;
    
    try {
        let deleted = 0;
        for (const ip of selectedRows) {
            const response = await fetch('/api/records/delete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ip })
            });
            
            if (response.ok) deleted++;
        }
        
        showToast(`Deleted ${deleted} record(s)`, 'success');
        selectedRows.clear();
        loadRecords();
    } catch (error) {
        console.error('Error deleting records:', error);
        showToast('Failed to delete records', 'error');
    }
}

// ━━ IMPORT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function openImportDialog() {
    document.getElementById('importFile').value = '';
    document.getElementById('importStatus').innerHTML = '';
    document.getElementById('importStatus').classList.remove('active');
    openDialog('importDialog');
}

async function performImport() {
    const fileInput = document.getElementById('importFile');
    
    if (!fileInput.files.length) {
        showToast('Select a file to import', 'warning');
        return;
    }
    
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', file.name.endsWith('.json') ? 'json' : 'csv');
    
    try {
        const response = await fetch('/api/import', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!data.success) {
            showImportStatus(`Error: ${data.error}`, 'error');
            return;
        }
        
        if (data.warning) {
            showImportStatus(
                `⚠️ Found conflicts: ${data.conflicts} IP conflicts, ${data.overlaps} subnet overlaps.\n\n` +
                `Imported ${data.imported} records anyway.`,
                'warning'
            );
        } else {
            showImportStatus(`✓ Successfully imported ${data.imported} records`, 'success');
        }
        
        setTimeout(() => {
            closeDialog('importDialog');
            loadRecords();
        }, 1500);
    } catch (error) {
        console.error('Error importing:', error);
        showImportStatus('Failed to import file', 'error');
    }
}

function showImportStatus(message, type) {
    const status = document.getElementById('importStatus');
    status.innerHTML = message;
    status.className = `import-status active ${type}`;
}

// ━━ EXPORT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function exportRecords() {
    const format = prompt('Export as:\n1. CSV\n2. JSON\n\nEnter 1 or 2:', '1');
    
    if (format === null) return;
    
    const type = format === '2' ? 'json' : 'csv';
    window.location.href = `/api/export?format=${type}`;
    showToast(`Exporting as ${type.toUpperCase()}...`, 'success');
}

// ━━ RECOVERY ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async function openRecoveryDialog() {
    openDialog('deletedDialog');
    loadDeletedRecords();
}

async function loadDeletedRecords() {
    try {
        const response = await fetch('/api/deleted');
        if (!response.ok) throw new Error('Failed to load deleted records');
        
        const data = await response.json();
        deletedRecords = data.data || [];
        
        renderDeletedList();
    } catch (error) {
        console.error('Error loading deleted records:', error);
        showToast('Error loading deleted records', 'error');
    }
}

function renderDeletedList() {
    const list = document.getElementById('deletedList');
    
    if (deletedRecords.length === 0) {
        list.innerHTML = '<p class="text-muted text-center" style="padding: 20px;">No deleted records</p>';
        return;
    }
    
    list.innerHTML = deletedRecords.map(record => `
        <div class="deleted-item">
            <div class="deleted-item-info">
                <div class="deleted-item-ip">${record.ip}</div>
                <div class="deleted-item-hostname">${record.hostname}</div>
            </div>
            <button class="btn btn-add deleted-item-btn" 
                    onclick="recoverDeleted('${record.ip}')">Recover</button>
        </div>
    `).join('');
}

async function recoverDeleted(ip) {
    try {
        const response = await fetch('/api/deleted/recover', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ip })
        });
        
        const data = await response.json();
        
        if (!data.success) {
            showToast(data.error || 'Failed to recover', 'error');
            return;
        }
        
        showToast('Record recovered', 'success');
        loadDeletedRecords();
        loadRecords();
    } catch (error) {
        console.error('Error recovering record:', error);
        showToast('Failed to recover record', 'error');
    }
}

async function clearAllDeleted() {
    if (!confirm('Clear all deleted records permanently?')) return;
    
    try {
        const response = await fetch('/api/deleted/clear', { method: 'POST' });
        const data = await response.json();
        
        if (!data.success) {
            showToast('Failed to clear', 'error');
            return;
        }
        
        showToast('Deleted records cleared', 'success');
        loadDeletedRecords();
    } catch (error) {
        console.error('Error clearing deleted:', error);
        showToast('Failed to clear deleted records', 'error');
    }
}

// ━━ SETTINGS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function openSettingsDialog() {
    document.getElementById('recordCount').textContent = `Total records: ${records.length}`;
    openDialog('settingsDialog');
}

// ━━ SUMMARY STATS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async function updateSummary() {
    try {
        const response = await fetch('/api/summary');
        if (!response.ok) throw new Error('Failed to load summary');
        
        const data = await response.json();
        const summary = data.data;
        
        document.getElementById('badge-total').textContent = `${summary.total} total`;
        document.getElementById('badge-active').textContent = `${summary.active} active`;
        document.getElementById('badge-inactive').textContent = `${summary.inactive} inactive`;
        document.getElementById('badge-reserved').textContent = `${summary.reserved} reserved`;
    } catch (error) {
        console.error('Error updating summary:', error);
    }
}

// ━━ DIALOGS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function openDialog(dialogId) {
    const dialog = document.getElementById(dialogId);
    dialog.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeDialog(dialogId) {
    const dialog = document.getElementById(dialogId);
    dialog.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Close modals when clicking outside
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
});

// ━━ TOAST NOTIFICATIONS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast active ${type}`;
    
    setTimeout(() => {
        toast.classList.remove('active');
    }, 3000);
}

// ━━ UTILITIES ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function isValidIP(ip) {
    const ipRegex = /^(\d{1,3}\.){3}\d{1,3}$/;
    if (!ipRegex.test(ip)) return false;
    
    const parts = ip.split('.').map(Number);
    return parts.every(part => part >= 0 && part <= 255);
}

// Load data on page focus (refresh when user switches back)
window.addEventListener('focus', () => {
    loadRecords();
    updateSummary();
});

"""
IP Management Tool - Web Version
Flask-based web application for managing IP addresses
Accessible via LAN: http://localhost:5000 or http://<your-ip>:5000
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import os
from datetime import datetime
from io import BytesIO
import csv

# Import existing modules
from modules import (
    load_records, add_record, update_record, delete_record, get_summary,
    search_records, sort_records, VALID_STATUSES,
    create_backup, cleanup_old_backups, save_deleted_record,
    get_deleted_records, clear_deleted_records,
    logger, log_error, log_info, log_warning,
    import_csv, import_json, detect_import_conflicts, detect_subnet_overlaps,
)

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# ── HOME PAGE ──────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Main application page"""
    return render_template('index.html')

# ── API: RECORDS ───────────────────────────────────────────────────────────

@app.route('/api/records', methods=['GET'])
def get_records():
    """Fetch all records with optional search/sort"""
    records = load_records()
    
    # Search filter
    search_query = request.args.get('search', '').lower()
    if search_query:
        records = search_records(records, search_query)
    
    # Sort
    sort_by = request.args.get('sort_by', 'ip')
    sort_rev = request.args.get('sort_rev', 'false').lower() == 'true'
    records = sort_records(records, sort_by, sort_rev)
    
    return jsonify({
        'success': True,
        'data': records,
        'count': len(records)
    })

@app.route('/api/records/<ip>', methods=['GET'])
def get_record(ip):
    """Get single record by IP"""
    records = load_records()
    record = next((r for r in records if r['ip'] == ip), None)
    
    if not record:
        return jsonify({'success': False, 'error': 'Record not found'}), 404
    
    return jsonify({'success': True, 'data': record})

@app.route('/api/records/add', methods=['POST'])
def api_add_record():
    """Add new record"""
    try:
        data = request.json
        result = add_record(
            data['ip'],
            data['hostname'],
            data['status'],
            data.get('notes', '')
        )
        
        if result:
            create_backup()
            log_info(f"Added record: {data['ip']}")
            return jsonify({'success': True, 'message': 'Record added'})
        else:
            return jsonify({'success': False, 'error': 'Failed to add record'}), 400
    except Exception as e:
        log_error("Error adding record", e)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/records/update', methods=['POST'])
def api_update_record():
    """Update existing record"""
    try:
        data = request.json
        result = update_record(
            data['ip'],
            data['hostname'],
            data['status'],
            data.get('notes', '')
        )
        
        if result:
            create_backup()
            log_info(f"Updated record: {data['ip']}")
            return jsonify({'success': True, 'message': 'Record updated'})
        else:
            return jsonify({'success': False, 'error': 'Record not found'}), 404
    except Exception as e:
        log_error("Error updating record", e)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/records/delete', methods=['POST'])
def api_delete_record():
    """Delete record (archive to deleted)"""
    try:
        data = request.json
        ip = data['ip']
        records = load_records()
        record = next((r for r in records if r['ip'] == ip), None)
        
        if not record:
            return jsonify({'success': False, 'error': 'Record not found'}), 404
        
        save_deleted_record(record)
        result = delete_record(ip)
        
        if result:
            create_backup()
            log_info(f"Deleted record: {ip}")
            return jsonify({'success': True, 'message': 'Record deleted'})
        else:
            return jsonify({'success': False, 'error': 'Failed to delete'}), 500
    except Exception as e:
        log_error("Error deleting record", e)
        return jsonify({'success': False, 'error': str(e)}), 500

# ── API: SUMMARY ───────────────────────────────────────────────────────────

@app.route('/api/summary', methods=['GET'])
def api_summary():
    """Get summary statistics"""
    records = load_records()
    summary = get_summary(records)
    
    return jsonify({
        'success': True,
        'data': summary
    })

# ── API: IMPORT/EXPORT ─────────────────────────────────────────────────────

@app.route('/api/import', methods=['POST'])
def api_import():
    """Import records from CSV or JSON"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if not file.filename:
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        import_type = request.form.get('type', 'csv')
        file_content = file.read().decode('utf-8')
        
        if import_type == 'json':
            imported = import_json(file_content)
        else:
            imported = import_csv(file_content)
        
        if not imported:
            return jsonify({'success': False, 'error': 'Import failed'}), 400
        
        # Check for conflicts
        records = load_records()
        conflicts = detect_import_conflicts(records, imported)
        overlaps = detect_subnet_overlaps(records, imported)
        
        if conflicts or overlaps:
            return jsonify({
                'success': True,
                'warning': True,
                'imported': len(imported),
                'conflicts': len(conflicts),
                'overlaps': len(overlaps),
                'data': {
                    'conflicts': conflicts,
                    'overlaps': overlaps
                }
            })
        
        # Auto-add all records
        for record in imported:
            add_record(record['ip'], record['hostname'], 
                      record['status'], record.get('notes', ''))
        
        create_backup()
        log_info(f"Imported {len(imported)} records")
        
        return jsonify({
            'success': True,
            'message': f'Imported {len(imported)} records',
            'imported': len(imported)
        })
    except Exception as e:
        log_error("Error importing", e)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export', methods=['GET'])
def api_export():
    """Export records as CSV"""
    try:
        records = load_records()
        export_format = request.args.get('format', 'csv')
        
        if export_format == 'json':
            output = BytesIO(json.dumps(records, indent=2).encode())
            filename = f"ip_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            mimetype = "application/json"
        else:
            output = BytesIO()
            writer = csv.DictWriter(output, fieldnames=['ip', 'hostname', 'status', 'notes', 'timestamp'])
            writer.writeheader()
            writer.writerows(records)
            output.seek(0)
            filename = f"ip_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            mimetype = "text/csv"
        
        output.seek(0)
        return send_file(output, mimetype=mimetype, as_attachment=True, download_name=filename)
    except Exception as e:
        log_error("Error exporting", e)
        return jsonify({'success': False, 'error': str(e)}), 500

# ── API: DELETED RECORDS ───────────────────────────────────────────────────

@app.route('/api/deleted', methods=['GET'])
def api_get_deleted():
    """Get all deleted records"""
    deleted = get_deleted_records()
    return jsonify({
        'success': True,
        'data': deleted,
        'count': len(deleted)
    })

@app.route('/api/deleted/recover', methods=['POST'])
def api_recover_deleted():
    """Recover deleted record"""
    try:
        data = request.json
        ip = data['ip']
        deleted = get_deleted_records()
        record = next((r for r in deleted if r['ip'] == ip), None)
        
        if not record:
            return jsonify({'success': False, 'error': 'Deleted record not found'}), 404
        
        # Re-add the record
        result = add_record(record['ip'], record['hostname'], 
                           record['status'], record.get('notes', ''))
        
        if result:
            create_backup()
            log_info(f"Recovered record: {ip}")
            return jsonify({'success': True, 'message': 'Record recovered'})
        else:
            return jsonify({'success': False, 'error': 'Failed to recover'}), 500
    except Exception as e:
        log_error("Error recovering record", e)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/deleted/clear', methods=['POST'])
def api_clear_deleted():
    """Clear all deleted records"""
    try:
        result = clear_deleted_records()
        if result:
            log_info("Cleared deleted records")
            return jsonify({'success': True, 'message': 'Deleted records cleared'})
        else:
            return jsonify({'success': False, 'error': 'Failed to clear'}), 500
    except Exception as e:
        log_error("Error clearing deleted records", e)
        return jsonify({'success': False, 'error': str(e)}), 500

# ── API: SETTINGS ──────────────────────────────────────────────────────────

@app.route('/api/settings', methods=['GET'])
def api_get_settings():
    """Get app settings"""
    settings = {
        'valid_statuses': VALID_STATUSES,
        'theme': 'dark'
    }
    return jsonify({'success': True, 'data': settings})

# ── ERROR HANDLERS ─────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'success': False, 'error': 'Server error'}), 500

# ── MAIN ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Create backup on startup
    try:
        create_backup()
        cleanup_old_backups(keep_count=10)
        log_info("Web server starting - backup created")
    except Exception as e:
        log_error("Failed to create startup backup", e)
    
    # Get local IP for display
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("\n" + "="*60)
    print("IP MANAGEMENT TOOL - WEB VERSION")
    print("="*60)
    print(f"🌐 Access via: http://localhost:5000")
    print(f"🌐 Or from LAN: http://{local_ip}:5000")
    print(f"📡 Hostname: {hostname}")
    print("="*60 + "\n")
    
    # Run Flask app (accessible on LAN)
    app.run(host='0.0.0.0', port=5000, debug=False)

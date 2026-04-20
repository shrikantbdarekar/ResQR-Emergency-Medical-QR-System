from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_mysqldb import MySQL
import qrcode
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'resqr_secret_key_2024'

# MySQL Configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'MySql@1234#$'
app.config['MYSQL_DB'] = 'resqr_db'
app.config['MYSQL_PORT'] = 3308
app.config['MYSQL_CHARSET'] = 'utf8mb4'
app.config['MYSQL_PORT'] = 3308
app.config['MYSQL_CHARSET'] = 'utf8mb4'
app.config['MYSQL_PORT'] = 3308

# Upload Configuration
UPLOAD_FOLDER = 'uploads'
QRCODE_FOLDER = 'static/qrcodes'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['QRCODE_FOLDER'] = QRCODE_FOLDER

mysql = MySQL(app)

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QRCODE_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        alt_phone = request.form.get('alt_phone', '')
        dob = request.form.get('dob')
        blood_group = request.form.get('blood_group')
        disease = request.form.get('disease')
        disease_details = request.form.get('disease_details', '')
        password = request.form.get('password')
        
        # Validation - all mandatory except disease_details and document
        if not all([name, address, phone, dob, blood_group, disease, password]):
            flash('Please fill all mandatory fields', 'danger')
            return redirect(url_for('register'))
        
        if len(phone) != 10 or not phone.isdigit():
            flash('Phone number must be 10 digits', 'danger')
            return redirect(url_for('register'))
        
        # Check if phone already exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE phone = %s", (phone,))
        if cur.fetchone():
            cur.close()
            flash('Phone number already registered', 'danger')
            return redirect(url_for('register'))
        cur.close()
        
        # Handle document upload (optional)
        document_path = None
        if 'document' in request.files:
            file = request.files['document']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"{phone}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                document_path = filepath
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Insert into database
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO users (name, address, phone, alt_phone, dob, blood_group, disease, disease_details, document_path, password, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pending')
        """, (name, address, phone, alt_phone, dob, blood_group, disease, disease_details, document_path, hashed_password))
        mysql.connection.commit()
        cur.close()
        
        flash('Registration successful! You can now login to check your status.', 'success')
        return redirect(url_for('user_login'))
    
    return render_template('register.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password FROM users WHERE phone = %s", (phone,))
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['user_phone'] = phone
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid phone number or password', 'danger')
    
    return render_template('user_login.html')

# User Dashboard
@app.route('/dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('user_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    
    if not user:
        session.clear()
        return redirect(url_for('user_login'))
    
    return render_template('user_dashboard.html', user=user)

# User Logout
@app.route('/logout')
def user_logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('user_login'))

# Download QR Code
@app.route('/download-qr')
def download_qr():
    if 'user_id' not in session:
        return redirect(url_for('user_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT qr_code_path, status FROM users WHERE id = %s", (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    
    if not user or user[1] != 'Approved' or not user[0]:
        flash('QR code not available', 'danger')
        return redirect(url_for('user_dashboard'))
    
    return send_file(user[0], as_attachment=True, download_name=f"resqr_{session['user_id']}.png")

# Download User's Document
@app.route('/download-document')
def download_document():
    if 'user_id' not in session:
        return redirect(url_for('user_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT document_path FROM users WHERE id = %s", (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    
    if not user or not user[0]:
        flash('No document uploaded', 'danger')
        return redirect(url_for('user_dashboard'))
    
    # Get original filename from path
    import os
    filename = os.path.basename(user[0])
    
    return send_file(user[0], as_attachment=True, download_name=filename)

# Admin Login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('admin_login.html')

# Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = cur.fetchall()
    cur.close()
    
    return render_template('admin_dashboard.html', users=users)

# Approve User
@app.route('/admin/approve/<int:user_id>')
def approve_user(user_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    # Get user data
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    # Create comprehensive QR data with all user information
    qr_data = f"""
╔══════════════════════════════════════╗
║      EMERGENCY CONTACT INFO          ║
╚══════════════════════════════════════╝

👤 NAME: {user[1]}
📍 ADDRESS: {user[2]}
📞 PHONE: {user[3]}
"""
    
    if user[4]:  # alt_phone
        qr_data += f"📱 ALT PHONE: {user[4]}\n"
    
    qr_data += f"""
🎂 DOB: {user[5]}
🩸 BLOOD GROUP: {user[6]}

⚕️ MEDICAL CONDITION: {user[7]}
"""
    
    if user[8]:  # disease_details
        qr_data += f"📋 DETAILS: {user[8]}\n"
    
    # Add URL for more info and document download
    qr_data += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌐 FULL INFO & DOCUMENT:
http://localhost:5000/user/{user_id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    # Generate QR Code with larger size to accommodate more data
    qr = qrcode.QRCode(
        version=None,  # Auto-determine version based on data
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_filename = f"qr_{user_id}.png"
    qr_path = os.path.join(app.config['QRCODE_FOLDER'], qr_filename)
    qr_img.save(qr_path)
    
    # Update database
    cur.execute("""
        UPDATE users SET status = 'Approved', qr_code_path = %s WHERE id = %s
    """, (f"static/qrcodes/{qr_filename}", user_id))
    mysql.connection.commit()
    cur.close()
    
    flash('User approved and QR code generated', 'success')
    return redirect(url_for('admin_dashboard'))

# Reject User
@app.route('/admin/reject/<int:user_id>')
def reject_user(user_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET status = 'Rejected' WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()
    
    flash('User rejected', 'warning')
    return redirect(url_for('admin_dashboard'))

# Admin Logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

# Admin Download User Document
@app.route('/admin/download-document/<int:user_id>')
def admin_download_document(user_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT document_path, name FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    
    if not user or not user[0]:
        flash('No document found for this user', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    # Get original filename from path
    import os
    filename = os.path.basename(user[0])
    
    return send_file(user[0], as_attachment=True, download_name=filename)

# User Details (QR Scan)
@app.route('/user/<int:user_id>')
def user_details(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s AND status = 'Approved'", (user_id,))
    user = cur.fetchone()
    cur.close()
    
    if not user:
        return "User not found or not approved", 404
    
    return render_template('user_details.html', user=user)

# Public Document Download (for QR scan page)
@app.route('/public/download-document/<int:user_id>')
def public_download_document(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT document_path, status FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    
    # Only allow download if user is approved
    if not user or user[1] != 'Approved' or not user[0]:
        return "Document not available", 404
    
    # Get original filename from path
    import os
    filename = os.path.basename(user[0])
    
    return send_file(user[0], as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True)

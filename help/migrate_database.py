import mysql.connector
from werkzeug.security import generate_password_hash

# Database configuration
config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'MySql@1234#',
    'database': 'resqr_db',
    'port': 3308
}

try:
    # Connect to database
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    print("Connected to database successfully!")
    
    # Check if columns already exist
    cursor.execute("SHOW COLUMNS FROM users LIKE 'disease_details'")
    disease_details_exists = cursor.fetchone()
    
    cursor.execute("SHOW COLUMNS FROM users LIKE 'password'")
    password_exists = cursor.fetchone()
    
    # Add disease_details column if it doesn't exist
    if not disease_details_exists:
        cursor.execute("ALTER TABLE users ADD COLUMN disease_details TEXT AFTER disease")
        print("✓ Added 'disease_details' column")
    else:
        print("✓ 'disease_details' column already exists")
    
    # Add password column if it doesn't exist
    if not password_exists:
        cursor.execute("ALTER TABLE users ADD COLUMN password VARCHAR(255) NOT NULL DEFAULT '' AFTER document_path")
        print("✓ Added 'password' column")
        
        # Set default password for existing users (they will need to reset)
        default_password = generate_password_hash('password123')
        cursor.execute("UPDATE users SET password = %s WHERE password = ''", (default_password,))
        print("✓ Set default password for existing users (password123)")
    else:
        print("✓ 'password' column already exists")
    
    # Make phone unique if not already
    cursor.execute("SHOW INDEXES FROM users WHERE Key_name = 'phone'")
    phone_index = cursor.fetchone()
    
    if not phone_index:
        try:
            cursor.execute("ALTER TABLE users ADD UNIQUE KEY (phone)")
            print("✓ Added unique constraint to phone column")
        except mysql.connector.Error as e:
            print(f"⚠ Could not add unique constraint (may have duplicates): {e}")
    else:
        print("✓ Phone column already has unique constraint")
    
    conn.commit()
    print("\n✅ Database migration completed successfully!")
    print("\nNote: Existing users can login with phone number and password: password123")
    
except mysql.connector.Error as e:
    print(f"❌ Database error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()

import MySQLdb

# Connect to MySQL server (without specifying database)
try:
    connection = MySQLdb.connect(
        host='localhost',
        user='root',
        password='MySql@1234#$',
        port=3308
    )
    
    cursor = connection.cursor()
    
    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS resqr_db")
    print("✓ Database 'resqr_db' created successfully!")
    
    # Use the database
    cursor.execute("USE resqr_db")
    
    # Create users table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        address TEXT NOT NULL,
        phone VARCHAR(10) NOT NULL,
        alt_phone VARCHAR(10),
        dob DATE NOT NULL,
        blood_group VARCHAR(5) NOT NULL,
        disease ENUM('Yes', 'No') NOT NULL,
        document_path VARCHAR(255),
        status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
        qr_code_path VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    cursor.execute(create_table_query)
    print("✓ Table 'users' created successfully!")
    
    connection.commit()
    cursor.close()
    connection.close()
    
    print("\n✅ Database setup completed successfully!")
    print("You can now run the application with: python app.py")
    
except MySQLdb.Error as e:
    print(f"❌ Error: {e}")

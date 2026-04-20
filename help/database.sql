-- Create Database
CREATE DATABASE IF NOT EXISTS resqr_db;
USE resqr_db;

-- Create Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    phone VARCHAR(10) NOT NULL UNIQUE,
    alt_phone VARCHAR(10),
    dob DATE NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    disease ENUM('Yes', 'No') NOT NULL,
    disease_details TEXT,
    document_path VARCHAR(255),
    password VARCHAR(255) NOT NULL,
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    qr_code_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

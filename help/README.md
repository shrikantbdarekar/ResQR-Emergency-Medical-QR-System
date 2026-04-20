# ResQr: Scan. Save. Support

Emergency QR-based system for storing and retrieving critical medical and personal information.

## Features

- User registration with medical details
- Admin approval system
- Automatic QR code generation
- Emergency information display via QR scan
- Responsive Bootstrap UI

## Technology Stack

- Frontend: HTML, CSS, Bootstrap, JavaScript
- Backend: Python (Flask)
- Database: MySQL
- QR Generation: qrcode library

## Project Structure

```
ResQr/
├── app.py                  # Main Flask application
├── database.sql            # Database schema
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── index.html
│   ├── register.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   └── user_details.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── register.js
│   ├── images/
│   └── qrcodes/           # Generated QR codes
└── uploads/               # Medical documents
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

### Installation Steps

1. Clone or download the project

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Setup MySQL Database:
   - Start MySQL server
   - Open MySQL command line or workbench
   - Run the database.sql file:
```bash
mysql -u root -p < database.sql
```

4. Configure Database Connection:
   - Open `app.py`
   - Update MySQL credentials if needed:
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Your MySQL password
app.config['MYSQL_DB'] = 'resqr_db'
```

5. Run the application:
```bash
python app.py
```

6. Access the application:
   - Open browser: http://localhost:5000

## Usage Guide

### User Registration
1. Navigate to Register page
2. Fill all required fields
3. Select blood group from dropdown
4. If you have a disease, select "Yes" and upload medical document
5. Submit form
6. Status will be "Pending" until admin approval

### Admin Panel
1. Go to Admin Login: http://localhost:5000/admin/login
2. Default credentials:
   - Username: `admin`
   - Password: `admin123`
3. View all registered users
4. Approve or reject users
5. Approved users get QR codes automatically

### QR Code Usage
1. After approval, QR code is generated
2. Admin can view/download QR from dashboard
3. Scan QR code with any QR scanner
4. Opens emergency information page
5. Displays: Name, Blood Group, Contact, Medical Info

## Test Scenario

1. Register a new user → Status = Pending
2. Login as admin
3. Approve the user → QR code generated
4. Click "View QR" to see the QR code
5. Scan QR or open URL: http://localhost:5000/user/1
6. Emergency information displayed

## Database Schema

### users table
- id (Primary Key)
- name
- address
- phone (10 digits)
- alt_phone
- dob (Date of Birth)
- blood_group (A+, A-, B+, B-, AB+, AB-, O+, O-)
- disease (Yes/No)
- document_path
- status (Pending/Approved/Rejected)
- qr_code_path
- created_at

## Security Features

- Input validation (frontend & backend)
- File type restrictions (PDF, JPG, PNG)
- Phone number validation (10 digits)
- Admin authentication
- Secure file uploads

## Bonus Features Implemented

- Search/filter capability in admin panel (table structure ready)
- Download QR code option
- Print emergency card functionality
- Responsive mobile-friendly design

## Troubleshooting

### MySQL Connection Error
- Ensure MySQL server is running
- Check credentials in app.py
- Verify database exists: `SHOW DATABASES;`

### Module Not Found Error
- Install missing packages: `pip install -r requirements.txt`

### QR Code Not Generating
- Check folder permissions for `static/qrcodes/`
- Ensure qrcode library is installed

### File Upload Issues
- Check folder permissions for `uploads/`
- Verify file size limits
- Ensure allowed file types

## Admin Credentials

- Username: admin
- Password: admin123

(Change these in production!)

## Support

For issues or questions, check the code comments or review the Flask documentation.

# Screenshots Guide

This folder contains screenshots for the ResQR project documentation.

## Required Screenshots

Please add the following screenshots to this folder:

### 1. `homepage.png`
- **What to capture:** The landing page (index.html)
- **URL:** http://localhost:5000/
- **Shows:** Hero section with "Scan. Save. Support" tagline and feature cards

### 2. `register.png`
- **What to capture:** User registration form
- **URL:** http://localhost:5000/register
- **Shows:** Complete registration form with all fields

### 3. `user-login.png`
- **What to capture:** User login page
- **URL:** http://localhost:5000/login
- **Shows:** Login form with phone and password fields

### 4. `user-dashboard.png`
- **What to capture:** User dashboard after login
- **URL:** http://localhost:5000/dashboard
- **Shows:** User profile, status, and QR code download option

### 5. `admin-login.png`
- **What to capture:** Admin login page
- **URL:** http://localhost:5000/admin/login
- **Shows:** Admin authentication form

### 6. `admin-dashboard.png`
- **What to capture:** Admin panel with user list
- **URL:** http://localhost:5000/admin/dashboard
- **Shows:** Table of registered users with approve/reject buttons

### 7. `qr-code.png`
- **What to capture:** Generated QR code (from admin dashboard or user dashboard)
- **Shows:** The actual QR code image with emergency information

### 8. `emergency-info.png`
- **What to capture:** Public emergency information page
- **URL:** http://localhost:5000/user/1 (after approving a user)
- **Shows:** Patient information displayed when QR is scanned

## How to Take Screenshots

### Method 1: Using Browser (Recommended)
1. Run the application: `python app.py`
2. Open browser and navigate to each URL
3. Press `F12` to open Developer Tools
4. Press `Ctrl + Shift + P` (Windows) or `Cmd + Shift + P` (Mac)
5. Type "screenshot" and select "Capture full size screenshot"
6. Save with the appropriate filename

### Method 2: Using Snipping Tool (Windows)
1. Press `Windows + Shift + S`
2. Select area to capture
3. Save with appropriate filename

### Method 3: Using Screenshot Tool (Mac)
1. Press `Cmd + Shift + 4`
2. Select area to capture
3. Save with appropriate filename

## Image Guidelines

- **Format:** PNG (preferred) or JPG
- **Resolution:** Minimum 1280x720px
- **File Size:** Keep under 500KB per image
- **Quality:** Clear, readable text and UI elements
- **Naming:** Use lowercase with hyphens (e.g., `admin-dashboard.png`)

## Optional Screenshots

You can also add:
- `qr-scan-mobile.png` - Mobile view of QR scanning
- `document-upload.png` - Document upload interface
- `approval-process.png` - Admin approving a user
- `error-validation.png` - Form validation errors

## After Adding Screenshots

Once you've added the screenshots, they will automatically appear in the main README.md file.

The README references them as:
```markdown
![Homepage](docs/screenshots/homepage.png)
```

No code changes needed - just add the images to this folder!

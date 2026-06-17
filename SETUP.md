# Digital Attendance System - Setup Guide

## Prerequisites

- Python 3.11 or higher
- MySQL 8.0+ or PostgreSQL 15+
- pip (Python package manager)
- Git (optional, for version control)

## Step 1: Database Setup

### For MySQL:

```bash
# Connect to MySQL
mysql -u root -p

# Run the schema
source migrations/schema.sql

# Or create database manually
CREATE DATABASE attendance_db;
USE attendance_db;
# Then run the SQL from migrations/schema.sql
```

### For PostgreSQL:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE attendance_db;

# Connect to the new database
\c attendance_db

# Run the schema (adapt SQL syntax for PostgreSQL)
```

## Step 2: Python Environment Setup

```bash
# Navigate to project directory
cd /home/gituya/CascadeProjects/digital-attendance

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

### Required .env Variables:

```
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=attendance_db
DB_PORT=3306

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production

# HMAC Configuration (for QR signing)
HMAC_SECRET_KEY=your-super-secret-hmac-key-change-in-production

# Application Settings
APP_NAME=Digital Attendance System
APP_DOMAIN=localhost:5000
```

### Generate Secure Keys:

```bash
# Generate JWT secret
python -c "import secrets; print(secrets.token_hex(32))"

# Generate HMAC secret
python -c "import secrets; print(secrets.token_hex(32))"
```

## Step 4: Run the Application

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the Flask development server
python run.py

# The application will be available at http://localhost:5000
```

## Step 5: Create Initial Admin User (Optional)

```bash
# Access Flask shell
python -c "from app import create_app; from app.models.user import User; app = create_app(); User.create('Admin User', 'admin@example.com', 'AdminPassword123', 'admin')"
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_auth.py

# Run with verbose output
python -m pytest -v tests/
```

## Troubleshooting

### Database Connection Error

**Problem**: `pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")`

**Solution**:
- Verify MySQL is running: `sudo service mysql status`
- Check database credentials in `.env`
- Ensure database exists: `mysql -u root -p -e "SHOW DATABASES;"`

### Port Already in Use

**Problem**: `Address already in use`

**Solution**:
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use a different port
python run.py --port 5001
```

### Module Not Found

**Problem**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### JWT Cookie Issues

**Problem**: Authentication not working

**Solution**:
- Clear browser cookies
- Check `JWT_SECRET_KEY` in `.env`
- Ensure cookies are enabled in browser

## Production Deployment

### Using Gunicorn + Nginx

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# For production, use systemd service or supervisor
```

### SSL/HTTPS with Let's Encrypt

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Configure Nginx with SSL
```

### Environment Variables for Production

```
FLASK_ENV=production
FLASK_DEBUG=False
JWT_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
```

## Database Backup

```bash
# Backup MySQL database
mysqldump -u root -p attendance_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
mysql -u root -p attendance_db < backup_20240101_120000.sql
```

## Monitoring and Logs

Logs are stored in `logs/attendance.log`

```bash
# View recent logs
tail -f logs/attendance.log

# View with timestamps
tail -f logs/attendance.log | grep "ERROR"
```

## API Documentation

All API endpoints are documented in the README.md file. Key endpoints:

- **Authentication**: `/api/auth/register`, `/api/auth/login`, `/api/auth/logout`
- **Student**: `/api/student/units`, `/api/student/attendance`, `/api/student/mark`
- **Lecturer**: `/api/lecturer/units`, `/api/sessions/start`, `/api/sessions/:id/qr`
- **Admin**: `/api/admin/users`, `/api/admin/units`, `/api/admin/reports/dashboard`

## Support

For issues or questions:
1. Check the logs: `tail -f logs/attendance.log`
2. Review the README.md for API documentation
3. Check database schema: `migrations/schema.sql`
4. Review test cases for usage examples: `tests/`

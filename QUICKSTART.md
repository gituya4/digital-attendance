# Digital Attendance System - Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
cd /home/gituya/CascadeProjects/digital-attendance
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Setup Database
```bash
# Create database
mysql -u root -p < migrations/schema.sql

# Or manually:
mysql -u root -p
CREATE DATABASE attendance_db;
USE attendance_db;
# Paste contents of migrations/schema.sql
```

### 3. Configure Environment
```bash
cp .env.example .env

# Edit .env with your database credentials:
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME=attendance_db
```

### 4. Run Application
```bash
python run.py
```

Visit: **http://localhost:5000**

---

## Test Accounts

### Create Test Users (Optional)

```bash
# Access Python shell
python -c "
from app import create_app
from app.models.user import User

app = create_app()

# Create student
User.create('Alice Johnson', 'alice@example.com', 'TestPassword123', 'student', registration_number='CS/MK/0792/09/23')

# Create lecturer
User.create('Dr. Smith', 'smith@example.com', 'TestPassword123', 'lecturer', staff_id='LEC001', department='Computer Science')

# Create admin
User.create('Admin User', 'admin@example.com', 'TestPassword123', 'admin')

print('Test users created!')
"
```

### Test Credentials:
- **Student**: alice@example.com / TestPassword123
- **Lecturer**: smith@example.com / TestPassword123
- **Admin**: admin@example.com / TestPassword123

---

## User Workflows

### Student Workflow
1. Register with registration number (format: CS/MK/0792/09/23)
2. Login to dashboard
3. View enrolled units with attendance percentage
4. Click FAB button (📱) to scan QR code
5. Allow camera access
6. Scan QR code from lecturer's session
7. Enter 4-digit PIN
8. Attendance marked ✓

### Lecturer Workflow
1. Register with staff ID and department
2. Login to dashboard
3. View assigned units
4. Click "Start Session" on a unit
5. Share PIN verbally with students
6. Display QR code to class
7. Watch live attendance list update in real-time
8. Click "Export CSV" to download attendance
9. Click "Close Session" when done

### Admin Workflow
1. Login to admin dashboard
2. Navigate sections using sidebar:
   - **Dashboard**: View statistics and at-risk students
   - **Users**: Create/manage students, lecturers, admins
   - **Units**: Create courses and assign lecturers
   - **Requests**: Review manual attendance correction requests
   - **Logs**: View system audit trail

---

## Key Features

### ✅ Implemented
- User registration and login with JWT
- Role-based access control (Student, Lecturer, Admin)
- Unit and enrollment management
- Attendance session creation
- QR code generation with HMAC signing
- PIN-based verification
- Admin user management
- Audit logging
- Professional UI with responsive design
- CSV export for attendance

### 🔄 In Progress
- QR code scanning with camera
- Real-time attendance updates (SSE)
- Manual attendance correction workflow
- PDF report generation
- Dashboard charts and statistics

### 📋 Planned
- Email notifications
- Mobile app
- Advanced reporting
- Biometric integration

---

## API Endpoints Quick Reference

### Authentication
```
POST   /api/auth/register      - Register new user
POST   /api/auth/login         - Login (returns JWT)
POST   /api/auth/logout        - Logout
GET    /api/auth/me            - Get current user
```

### Student
```
GET    /api/student/units      - Get enrolled units
GET    /api/student/attendance - Get attendance history
POST   /api/student/mark       - Mark attendance (QR + PIN)
POST   /api/student/request    - Submit correction request
```

### Lecturer
```
GET    /api/lecturer/units     - Get assigned units
POST   /api/sessions/start     - Start attendance session
GET    /api/sessions/:id/qr    - Get QR code (auto-rotates)
GET    /api/sessions/:id/live  - Live attendance stream (SSE)
POST   /api/sessions/:id/close - Close session
GET    /api/sessions/:id/export - Export CSV
```

### Admin
```
GET    /api/admin/users        - List users
POST   /api/admin/users        - Create user
PUT    /api/admin/users/:id    - Edit user
DELETE /api/admin/users/:id    - Deactivate user
GET    /api/admin/units        - List units
POST   /api/admin/units        - Create unit
POST   /api/admin/units/:id/assign-lecturer
POST   /api/admin/units/:id/enroll-student
GET    /api/admin/requests     - Get correction requests
PUT    /api/admin/requests/:id - Review request
GET    /api/admin/reports/dashboard - Dashboard stats
GET    /api/admin/logs         - Audit logs
```

---

## Troubleshooting

### "Can't connect to MySQL"
```bash
# Start MySQL
sudo service mysql start

# Check status
sudo service mysql status
```

### "Port 5000 already in use"
```bash
# Find and kill process
lsof -i :5000
kill -9 <PID>
```

### "Module not found"
```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "JWT cookie not working"
```bash
# Clear browser cookies
# Check .env has JWT_SECRET_KEY set
# Restart Flask app
```

---

## File Structure

```
digital-attendance/
├── app/
│   ├── models/          # Database models
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   ├── templates/       # HTML pages
│   └── static/          # CSS, JS, images
├── migrations/          # Database schema
├── tests/               # Unit tests
├── run.py              # Entry point
├── requirements.txt    # Dependencies
└── .env               # Configuration
```

---

## Next Steps

1. **Setup Database**: Run migrations/schema.sql
2. **Configure .env**: Set database credentials
3. **Run Application**: `python run.py`
4. **Create Test Data**: Register users or use test accounts
5. **Test Workflows**: Try student, lecturer, and admin flows
6. **Review Code**: Check app/routes/ for API implementation
7. **Run Tests**: `python -m pytest tests/`

---

## Support Resources

- **README.md**: Full project documentation
- **SETUP.md**: Detailed setup instructions
- **PROGRESS.md**: Development status and roadmap
- **migrations/schema.sql**: Database schema
- **tests/**: Example test cases

---

## Production Deployment

For production, see SETUP.md section "Production Deployment" for:
- Gunicorn + Nginx setup
- SSL/HTTPS with Let's Encrypt
- Environment variables
- Database backups

---

## Security Notes

✅ Passwords hashed with bcrypt (12 rounds)
✅ JWT in httpOnly cookies
✅ HMAC-signed QR tokens
✅ Rate limiting on login
✅ SQL injection prevention
✅ CORS configured
✅ Audit logging enabled

For production, also enable:
- HTTPS/SSL
- CSRF protection
- Security headers
- Database backups

---

**Ready to go!** 🚀

Questions? Check the documentation files or review the code comments.

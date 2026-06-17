# Digital Class Attendance List Web Application

A production-grade, secure web system for managing university class attendance using QR codes and PIN verification.

## Project Overview

This system replaces manual, paper-based attendance tracking with a dual-factor digital verification process. It supports three user roles:
- **Students**: Scan QR codes and enter PINs to mark attendance
- **Lecturers**: Create attendance sessions, generate QR codes, and view live attendance
- **Administrators**: Manage users, units, and generate institutional reports

## Tech Stack

- **Backend**: Python 3.11+ with Flask
- **Database**: MySQL/PostgreSQL
- **Authentication**: JWT (JSON Web Tokens) with bcrypt password hashing
- **QR Code**: Server-side generation with client-side scanning (ZXing JS)
- **Real-Time**: Server-Sent Events (SSE) for live updates
- **Security**: HTTPS, CSRF protection, rate limiting, token expiry

## Installation

### Prerequisites
- Python 3.11+
- MySQL 8.0+ or PostgreSQL 15+
- pip (Python package manager)

### Setup Steps

1. **Clone/Extract the project**
   ```bash
   cd /home/gituya/CascadeProjects/digital-attendance
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**
   - Create a MySQL database:
     ```bash
     mysql -u root -p < migrations/schema.sql
     ```
   - Update `.env` with your database credentials

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and update:
   - `DATABASE_URL`: Your database connection string
   - `JWT_SECRET_KEY`: A strong random secret (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `HMAC_SECRET_KEY`: Another strong random secret for QR signing

6. **Run the application**
   ```bash
   python run.py
   ```

The application will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and receive JWT
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user info

### Student Routes
- `GET /api/student/units` - Get enrolled units with attendance %
- `GET /api/student/attendance` - Get attendance history
- `POST /api/student/mark` - Mark attendance with QR + PIN
- `POST /api/student/request` - Submit manual correction request

### Lecturer Routes
- `GET /api/lecturer/units` - Get assigned units
- `POST /api/sessions/start` - Start attendance session
- `GET /api/sessions/:id/qr` - Get current QR token (auto-rotates every 30s)
- `GET /api/sessions/:id/live` - SSE stream for live attendance
- `POST /api/sessions/:id/close` - End session
- `GET /api/sessions/:id/export` - Export attendance as CSV

### Admin Routes
- `GET /api/admin/users` - List all users
- `POST /api/admin/users` - Create user
- `PUT /api/admin/users/:id` - Edit user
- `DELETE /api/admin/users/:id` - Deactivate user
- `GET /api/admin/units` - List all units
- `POST /api/admin/units` - Create unit
- `POST /api/admin/units/:id/assign-lecturer` - Assign lecturer to unit
- `POST /api/admin/units/:id/enroll-student` - Enroll student in unit
- `GET /api/admin/requests` - Get correction requests
- `PUT /api/admin/requests/:id` - Review correction request
- `GET /api/admin/reports/dashboard` - Dashboard statistics
- `GET /api/admin/logs` - Audit logs

## Security Features

✓ Passwords hashed with bcrypt (12 salt rounds)
✓ JWT stored in httpOnly, Secure, SameSite cookies
✓ Server-side input validation and sanitization
✓ Parameterized SQL queries (no injection)
✓ HMAC-SHA256 signed QR tokens
✓ 30-second QR token expiry (screenshot prevention)
✓ Rate limiting on login (5 attempts per 10 minutes)
✓ CORS configured for same-origin only
✓ Role-based access control (RBAC) on all routes
✓ Comprehensive audit logging

## Attendance Validation Pipeline

When a student submits a QR code + PIN, the system performs 6 validation checks:

1. **HMAC Signature Verification** - Ensure QR code hasn't been tampered with
2. **Token Timestamp Check** - Verify QR code is not older than 30 seconds
3. **Session Status Check** - Verify session is still active
4. **PIN Validation** - Verify submitted PIN matches session PIN
5. **Duplicate Check** - Prevent marking attendance twice for same session
6. **Enrollment Check** - Verify student is enrolled in the unit

All checks must pass for attendance to be recorded.

## Database Schema

The system uses 8 core tables:
- `users` - All user accounts (students, lecturers, admins)
- `units` - Courses/units
- `lecturer_units` - Lecturer-unit assignments
- `enrollments` - Student-unit enrollments
- `sessions` - Attendance sessions
- `attendance_records` - Marked attendance
- `correction_requests` - Manual attendance correction requests
- `audit_log` - System audit trail

All tables use foreign key constraints and proper indexing for performance.

## Development Notes

- All code follows PEP 8 style guidelines
- Type hints used throughout Python code
- No hardcoded secrets (use `.env`)
- Comprehensive error handling and logging
- Ready for production deployment with Gunicorn + Nginx

## Deployment

For production deployment:

1. Set `FLASK_ENV=production` in `.env`
2. Use Gunicorn as WSGI server:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```
3. Configure Nginx as reverse proxy with SSL (Let's Encrypt)
4. Use a production database (MySQL 8.0+)
5. Set strong secrets in `.env`

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## License

Kabarak University - CS/MK/0792/09/23 | Peter Gituya Ndono

## Support

For issues or questions, contact the development team.

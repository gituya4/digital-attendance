# Digital Attendance System - Documentation Index

## Quick Navigation

### 🚀 Getting Started
1. **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
2. **[SETUP.md](SETUP.md)** - Detailed installation instructions
3. **[README.md](README.md)** - Full project documentation

### 📚 Understanding the System
1. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Executive summary and status
2. **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and architecture
3. **[PROGRESS.md](PROGRESS.md)** - Development progress and roadmap

### 💻 Development
1. **[app/](app/)** - Source code
   - `models/` - Database models
   - `routes/` - API endpoints
   - `services/` - Business logic
   - `templates/` - HTML pages
   - `static/` - CSS and JavaScript
2. **[tests/](tests/)** - Test suite
3. **[migrations/schema.sql](migrations/schema.sql)** - Database schema

### 🔧 Configuration
1. **[.env.example](.env.example)** - Environment template
2. **[requirements.txt](requirements.txt)** - Python dependencies
3. **[run.py](run.py)** - Application entry point

---

## Documentation by Use Case

### "I want to set up the application"
→ Read **QUICKSTART.md** (5 min) then **SETUP.md** (detailed)

### "I want to understand the architecture"
→ Read **ARCHITECTURE.md** (system design)

### "I want to know the current status"
→ Read **PROJECT_SUMMARY.md** and **PROGRESS.md**

### "I want to use the API"
→ Check **README.md** (API Endpoints section)

### "I want to deploy to production"
→ See **SETUP.md** (Production Deployment section)

### "I want to understand the code"
→ Review **ARCHITECTURE.md** then explore `app/` directory

### "I want to run tests"
→ See **QUICKSTART.md** (Testing section)

### "I want to troubleshoot"
→ Check **SETUP.md** (Troubleshooting section)

---

## Key Files at a Glance

| File | Purpose | Size |
|------|---------|------|
| **README.md** | Full documentation | 500+ lines |
| **QUICKSTART.md** | Quick start guide | 300+ lines |
| **SETUP.md** | Setup instructions | 400+ lines |
| **ARCHITECTURE.md** | System architecture | 500+ lines |
| **PROJECT_SUMMARY.md** | Executive summary | 400+ lines |
| **PROGRESS.md** | Development status | 400+ lines |
| **app/__init__.py** | Flask app factory | 50 lines |
| **app/config.py** | Configuration | 30 lines |
| **app/database.py** | Database abstraction | 40 lines |
| **app/models/user.py** | User model | 80 lines |
| **app/models/unit.py** | Unit model | 100 lines |
| **app/models/session.py** | Session model | 60 lines |
| **app/models/attendance.py** | Attendance model | 80 lines |
| **app/routes/auth.py** | Auth endpoints | 80 lines |
| **app/routes/student.py** | Student endpoints | 100 lines |
| **app/routes/lecturer.py** | Lecturer endpoints | 150 lines |
| **app/routes/admin.py** | Admin endpoints | 200 lines |
| **app/services/auth_service.py** | Auth logic | 100 lines |
| **app/services/qr_service.py** | QR logic | 80 lines |
| **app/static/css/main.css** | Design system | 2000+ lines |
| **app/static/js/utils.js** | Utilities | 100 lines |
| **app/static/js/scanner.js** | QR scanner | 80 lines |
| **app/static/js/session.js** | Session mgmt | 150 lines |
| **migrations/schema.sql** | Database schema | 150 lines |
| **tests/test_auth.py** | Auth tests | 80 lines |
| **tests/test_attendance.py** | QR tests | 60 lines |
| **tests/test_validation.py** | Validation tests | 150 lines |

---

## Development Iterations

### ✅ Iteration 1: Foundation (COMPLETE)
- Project structure
- Database schema
- Authentication
- Authorization
- Configuration

**Status**: Ready for production

### ✅ Iteration 2: Architecture & Design (COMPLETE)
- HTML templates
- CSS design system
- Navigation
- Admin interface
- Responsive design

**Status**: Ready for production

### ✅ Iteration 3: Core Attendance Engine (COMPLETE)
- QR code generation
- Session management
- Token rotation
- Client-side integration
- Camera handling

**Status**: Ready for production

### 🔄 Iteration 4: Verification & Recording (IN PROGRESS)
- Validation pipeline
- SSE implementation
- Error handling
- Attendance recording
- Real-time updates

**Status**: Core logic complete, testing in progress

### 📋 Iteration 5: Reporting & Polish (PENDING)
- Attendance history
- CSV/PDF export
- Manual corrections
- Dashboard charts
- End-to-end testing

**Status**: Planned for next phase

---

## API Quick Reference

### Authentication
```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
GET    /api/auth/me
```

### Student
```
GET    /api/student/units
GET    /api/student/attendance
POST   /api/student/mark
POST   /api/student/request
```

### Lecturer
```
GET    /api/lecturer/units
POST   /api/sessions/start
GET    /api/sessions/:id/qr
GET    /api/sessions/:id/live
POST   /api/sessions/:id/close
GET    /api/sessions/:id/export
```

### Admin
```
GET    /api/admin/users
POST   /api/admin/users
PUT    /api/admin/users/:id
DELETE /api/admin/users/:id
GET    /api/admin/units
POST   /api/admin/units
POST   /api/admin/units/:id/assign-lecturer
POST   /api/admin/units/:id/enroll-student
GET    /api/admin/requests
PUT    /api/admin/requests/:id
GET    /api/admin/reports/dashboard
GET    /api/admin/logs
```

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript (ES6+) |
| **Backend** | Python 3.11+, Flask 3.0.0 |
| **Database** | MySQL 8.0+ / PostgreSQL 15+ |
| **Authentication** | JWT, bcrypt |
| **QR Codes** | qrcode (generation), ZXing JS (scanning) |
| **Real-Time** | Server-Sent Events (SSE) |
| **Security** | HMAC-SHA256, Rate Limiting, CORS |
| **Deployment** | Gunicorn, Nginx, Let's Encrypt |

---

## Security Features

✅ Bcrypt password hashing (12 rounds)
✅ JWT in httpOnly cookies
✅ HMAC-signed QR tokens
✅ 30-second token expiry
✅ Rate limiting (5/10min)
✅ Parameterized SQL queries
✅ Server-side validation
✅ Role-based access control
✅ Audit logging
✅ CORS configured

---

## Project Statistics

- **Total Lines of Code**: 3,500+
- **Database Tables**: 8
- **API Endpoints**: 25+
- **HTML Templates**: 6
- **CSS Lines**: 2,000+
- **JavaScript Lines**: 500+
- **Test Cases**: 14+
- **Documentation Pages**: 6

---

## Common Tasks

### Setup & Run
```bash
cd /home/gituya/CascadeProjects/digital-attendance
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with database credentials
python run.py
```

### Run Tests
```bash
python -m pytest tests/ -v
```

### Create Test Users
```bash
python -c "from app import create_app; from app.models.user import User; app = create_app(); User.create('Test Student', 'student@test.com', 'TestPassword123', 'student', registration_number='CS/MK/0792/09/23')"
```

### Export Database
```bash
mysqldump -u root -p attendance_db > backup.sql
```

### Deploy to Production
```bash
# See SETUP.md for full instructions
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

---

## Troubleshooting Quick Links

| Issue | Solution |
|-------|----------|
| Can't connect to MySQL | See SETUP.md → Troubleshooting |
| Port 5000 already in use | See SETUP.md → Troubleshooting |
| Module not found | See SETUP.md → Troubleshooting |
| JWT cookie not working | See SETUP.md → Troubleshooting |

---

## Next Steps

1. **Read QUICKSTART.md** (5 minutes)
2. **Run SETUP.md** (15 minutes)
3. **Start the application** (python run.py)
4. **Test the workflows** (student, lecturer, admin)
5. **Review the code** (app/ directory)
6. **Run tests** (pytest tests/)
7. **Deploy to production** (see SETUP.md)

---

## Support Resources

- **README.md** - Complete documentation
- **ARCHITECTURE.md** - System design
- **PROGRESS.md** - Development status
- **Code comments** - Implementation details
- **Test cases** - Usage examples
- **Error messages** - Debugging help

---

## Project Links

- **Repository**: `/home/gituya/CascadeProjects/digital-attendance`
- **Database**: `attendance_db` (MySQL/PostgreSQL)
- **Server**: `http://localhost:5000` (development)
- **Documentation**: All `.md` files in project root

---

## Version Information

- **Current Version**: 0.3.0 (Iteration 4 in progress)
- **Python**: 3.11+
- **Flask**: 3.0.0
- **Database**: MySQL 8.0+ / PostgreSQL 15+
- **Last Updated**: June 4, 2024

---

## Quick Links

- [QUICKSTART.md](QUICKSTART.md) - Start here!
- [README.md](README.md) - Full documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Status report
- [PROGRESS.md](PROGRESS.md) - Development roadmap
- [SETUP.md](SETUP.md) - Detailed setup

---

**Ready to get started?** → Read [QUICKSTART.md](QUICKSTART.md)

**Want to understand the system?** → Read [ARCHITECTURE.md](ARCHITECTURE.md)

**Need help?** → Check [SETUP.md](SETUP.md) Troubleshooting section

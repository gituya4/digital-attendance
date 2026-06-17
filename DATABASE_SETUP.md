# MySQL Database Setup & Configuration

## ✅ Database Setup Complete

The MySQL database has been successfully created and configured with test data.

---

## Database Information

**Database Name**: `attendance_db`
**Host**: `localhost`
**Port**: `3306`
**User**: `root`
**Password**: `Root@1234`

---

## Database Tables Created

The following 8 tables have been created:

1. **users** - User accounts (students, lecturers, admins)
2. **units** - Courses/units
3. **lecturer_units** - Lecturer-unit assignments
4. **enrollments** - Student-unit enrollments
5. **sessions** - Attendance sessions
6. **attendance_records** - Marked attendance
7. **correction_requests** - Manual correction requests
8. **audit_log** - System audit trail

---

## Test Users Created

### Students
| Email | Password | Reg # |
|-------|----------|-------|
| alice@example.com | TestPassword123 | CS/MK/0792/09/23 |
| bob@example.com | TestPassword123 | CS/MK/0793/09/23 |

### Lecturers
| Email | Password | Staff ID |
|-------|----------|----------|
| sarah@example.com | TestPassword123 | LEC001 |
| james@example.com | TestPassword123 | LEC002 |

### Admin
| Email | Password |
|-------|----------|
| admin@example.com | TestPassword123 |

---

## Test Units Created

| Code | Name | Department |
|------|------|-----------|
| CS101 | Introduction to Computer Science | Computer Science |
| CS102 | Data Structures | Computer Science |
| IT101 | Network Fundamentals | Information Technology |

---

## Verification Results

✅ **MySQL Connection**: Successful (Version 8.0.46)
✅ **Users Created**: 5 users (2 students, 2 lecturers, 1 admin)
✅ **Units Created**: 3 units
✅ **Login Tests**: All 3 roles (student, lecturer, admin) login successful

---

## Configuration Files

### .env File
The `.env` file has been created with the following database configuration:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=Root@1234
DB_NAME=attendance_db
DB_PORT=3306
```

**Location**: `/home/gituya/CascadeProjects/digital-attendance/.env`

---

## How to Connect to MySQL

### Command Line
```bash
mysql -u root -pRoot@1234 -h localhost attendance_db
```

### View Tables
```bash
mysql -u root -pRoot@1234 -e "USE attendance_db; SHOW TABLES;"
```

### View Users
```bash
mysql -u root -pRoot@1234 -e "USE attendance_db; SELECT user_id, full_name, email, role FROM users;"
```

### View Units
```bash
mysql -u root -pRoot@1234 -e "USE attendance_db; SELECT * FROM units;"
```

---

## Running the Application

### 1. Activate Virtual Environment
```bash
cd /home/gituya/CascadeProjects/digital-attendance
source venv/bin/activate
```

### 2. Start the Application
```bash
python3 run.py
```

### 3. Access the Application
```
http://localhost:5000
```

### 4. Login with Test Account
- **Email**: alice@example.com (or any test account)
- **Password**: TestPassword123

---

## Testing Workflows

### Student Workflow
1. Login as: alice@example.com / TestPassword123
2. View enrolled units
3. Test QR scanner (requires HTTPS)
4. View attendance history

### Lecturer Workflow
1. Login as: sarah@example.com / TestPassword123
2. View assigned units
3. Start attendance session
4. View QR code and PIN
5. Export attendance

### Admin Workflow
1. Login as: admin@example.com / TestPassword123
2. Create/manage users
3. Create units
4. Assign lecturers
5. Enroll students
6. View reports

---

## Database Backup

### Backup Database
```bash
mysqldump -u root -pRoot@1234 attendance_db > backup.sql
```

### Restore Database
```bash
mysql -u root -pRoot@1234 attendance_db < backup.sql
```

---

## Troubleshooting

### "Can't connect to MySQL"
```bash
# Check if MySQL is running
sudo service mysql status

# Start MySQL if not running
sudo service mysql start
```

### "Access denied for user 'root'"
```bash
# Verify password is correct
mysql -u root -pRoot@1234 -e "SELECT 1;"
```

### "Database doesn't exist"
```bash
# Recreate database
mysql -u root -pRoot@1234 < migrations/schema.sql
```

### "Table doesn't exist"
```bash
# Verify tables were created
mysql -u root -pRoot@1234 -e "USE attendance_db; SHOW TABLES;"

# If missing, run schema again
mysql -u root -pRoot@1234 < migrations/schema.sql
```

---

## Database Statistics

| Metric | Value |
|--------|-------|
| Total Users | 5 |
| Students | 2 |
| Lecturers | 2 |
| Admins | 1 |
| Total Units | 3 |
| Total Enrollments | 0 |
| Total Sessions | 0 |
| Total Attendance Records | 0 |

---

## Next Steps

1. ✅ Database created and configured
2. ✅ Test users created
3. ✅ Test units created
4. ⏭️ Start application: `python3 run.py`
5. ⏭️ Test student workflow
6. ⏭️ Test lecturer workflow
7. ⏭️ Test admin workflow
8. ⏭️ Deploy to production

---

## Important Notes

⚠️ **Development Only**: These test credentials are for development/testing only. Change them before production deployment.

✅ **Password Security**: All passwords are hashed with bcrypt (12 salt rounds) in the database.

✅ **Database Integrity**: Foreign key constraints are enabled to maintain data integrity.

✅ **Audit Logging**: All user actions are logged in the `audit_log` table.

---

## Support

For database issues:
1. Check MySQL is running: `sudo service mysql status`
2. Verify credentials in `.env` file
3. Check database exists: `mysql -u root -pRoot@1234 -e "SHOW DATABASES;"`
4. Check tables exist: `mysql -u root -pRoot@1234 -e "USE attendance_db; SHOW TABLES;"`
5. Review error logs: `tail -f /var/log/mysql/error.log`

---

**Status**: ✅ Database is ready for testing and development!

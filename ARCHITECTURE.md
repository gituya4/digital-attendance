# Digital Attendance System - Architecture Documentation

## System Overview

The Digital Attendance System is a full-stack web application built with Flask (backend) and vanilla JavaScript (frontend). It implements a secure, production-grade attendance tracking system using QR codes and PIN verification.

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  HTML5 Templates (Jinja2)                            │   │
│  │  - Login/Register                                    │   │
│  │  - Student Dashboard (Units + QR Scanner)            │   │
│  │  - Lecturer Dashboard (Session Management)           │   │
│  │  - Admin Dashboard (Multi-section Management)        │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  JavaScript (ES6+)                                   │   │
│  │  - utils.js (API wrapper, Toast, Auth)              │   │
│  │  - scanner.js (QR scanning with ZXing)              │   │
│  │  - session.js (Session management, SSE)             │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  CSS3 (Custom Design System)                         │   │
│  │  - Variables (colors, spacing, shadows)              │   │
│  │  - Components (buttons, cards, forms, tables)        │   │
│  │  - Responsive Grid System                            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTP/HTTPS
┌─────────────────────────────────────────────────────────────┐
│                     API LAYER (Flask)                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Routes (Blueprints)                                 │   │
│  │  - auth.py (Register, Login, Logout)                │   │
│  │  - student.py (Units, Attendance, Marking)          │   │
│  │  - lecturer.py (Sessions, QR, Live, Export)         │   │
│  │  - admin.py (Users, Units, Requests, Reports)       │   │
│  │  - pages.py (HTML Template Serving)                 │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Services (Business Logic)                           │   │
│  │  - auth_service.py (Validation, Registration)        │   │
│  │  - qr_service.py (QR Generation, HMAC Signing)      │   │
│  │  - report_service.py (CSV/PDF Generation)           │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Middleware & Utilities                              │   │
│  │  - JWT Authentication (Flask-JWT-Extended)           │   │
│  │  - Rate Limiting (Flask-Limiter)                     │   │
│  │  - CORS (Flask-CORS)                                 │   │
│  │  - Role-Based Access Control (Decorators)            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓ SQL
┌─────────────────────────────────────────────────────────────┐
│                  DATA LAYER (Database)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Models (ORM-like Abstraction)                       │   │
│  │  - User (Authentication, Profiles)                   │   │
│  │  - Unit (Courses, Assignments)                       │   │
│  │  - Session (Attendance Sessions)                     │   │
│  │  - Attendance (Marked Attendance Records)            │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Database (MySQL/PostgreSQL)                         │   │
│  │  - 8 Core Tables                                     │   │
│  │  - Foreign Key Constraints                           │   │
│  │  - Proper Indexing                                   │   │
│  │  - Audit Logging                                     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Authentication & Authorization

**Flow:**
```
User Input (Email + Password)
    ↓
AuthService.login()
    ├─ Fetch user from database
    ├─ Verify bcrypt password hash
    └─ Return user data
    ↓
JWT Token Generation
    ├─ Create token with user_id, role, name
    ├─ Set 8-hour expiry
    └─ Store in httpOnly cookie
    ↓
Protected Routes
    ├─ Verify JWT on every request
    ├─ Extract role from claims
    └─ Enforce role-based access
```

**Security Measures:**
- Bcrypt hashing (12 salt rounds)
- JWT in httpOnly, Secure, SameSite cookies
- Rate limiting (5 attempts per 10 minutes)
- Server-side session validation

### 2. QR Code & PIN System

**Generation Flow:**
```
Lecturer Starts Session
    ↓
Session Created in Database
    ├─ session_id
    ├─ unit_id
    ├─ lecturer_id
    ├─ session_pin (4-digit random)
    └─ status: 'active'
    ↓
QR Token Generation
    ├─ Payload: {session_id, timestamp}
    ├─ HMAC-SHA256 Sign with secret key
    ├─ Base64 encode
    └─ Generate QR code image
    ↓
Token Rotation (Every 30 seconds)
    ├─ New token generated
    ├─ Old token invalidated
    ├─ QR image updated
    └─ Sent to lecturer's browser via polling
```

**Verification Flow:**
```
Student Scans QR Code
    ↓
QRScanner.scan() (ZXing JS)
    ├─ Decode QR payload
    └─ Extract token
    ↓
Student Enters PIN
    ↓
POST /api/student/mark
    ├─ Token: {payload, signature}
    └─ PIN: 4-digit code
    ↓
Server-Side Validation (6 Checks)
    1. HMAC Signature Verification
       └─ Re-compute HMAC, compare signatures
    2. Token Timestamp Check
       └─ Verify token < 30 seconds old
    3. Session Status Check
       └─ Verify session is 'active'
    4. PIN Validation
       └─ Verify PIN matches session_pin
    5. Duplicate Check
       └─ Verify student hasn't marked for this session
    6. Enrollment Check
       └─ Verify student enrolled in unit
    ↓
All Checks Pass?
    ├─ YES: Insert attendance record
    │       └─ Push SSE update to lecturer
    └─ NO: Return error message
```

### 3. Real-Time Updates (SSE)

**Architecture:**
```
Lecturer Dashboard
    ├─ QR Refresh: Polling every 5 seconds
    │  └─ GET /api/sessions/:id/qr
    │     └─ Returns new QR + countdown
    │
    └─ Live Attendance: Server-Sent Events
       └─ GET /api/sessions/:id/live
          ├─ Opens persistent connection
          ├─ Listens for attendance events
          └─ Updates list in real-time
```

**Event Flow:**
```
Student Marks Attendance
    ↓
Attendance Record Inserted
    ↓
SSE Event Pushed to Lecturer
    ├─ Student name
    ├─ Registration number
    └─ Timestamp
    ↓
Lecturer's Browser Receives Event
    ├─ Parse JSON
    ├─ Animate new entry
    └─ Update attendance count
```

### 4. Database Schema

**Core Tables:**

```sql
users
├─ user_id (PK)
├─ full_name
├─ email (UNIQUE)
├─ password_hash (bcrypt)
├─ role (student|lecturer|admin)
├─ registration_number (students)
├─ staff_id (lecturers)
├─ department
├─ is_active
└─ created_at

units
├─ unit_id (PK)
├─ unit_code (UNIQUE)
├─ unit_name
├─ department
├─ semester
└─ academic_year

lecturer_units (Junction)
├─ id (PK)
├─ lecturer_id (FK → users)
└─ unit_id (FK → units)

enrollments (Junction)
├─ id (PK)
├─ student_id (FK → users)
└─ unit_id (FK → units)

sessions
├─ session_id (PK)
├─ unit_id (FK → units)
├─ lecturer_id (FK → users)
├─ session_pin (CHAR 4)
├─ current_token (VARCHAR 512)
├─ token_generated_at
├─ status (active|closed)
├─ start_time
└─ end_time

attendance_records
├─ record_id (PK)
├─ session_id (FK → sessions)
├─ student_id (FK → users)
├─ unit_id (FK → units)
├─ marked_at
└─ status (present|manual)

correction_requests
├─ request_id (PK)
├─ student_id (FK → users)
├─ session_id (FK → sessions)
├─ reason
├─ status (pending|approved|rejected)
├─ admin_comment
├─ submitted_at
└─ reviewed_at

audit_log
├─ log_id (PK)
├─ user_id (FK → users, nullable)
├─ action
├─ detail
├─ ip_address
└─ timestamp
```

---

## Request/Response Flow

### Example: Student Marks Attendance

**Request:**
```http
POST /api/student/mark
Content-Type: application/json
Cookie: access_token_cookie=eyJ0eXAi...

{
  "token": "eyJzZXNzaW9uX2lkIjogMSwgInRpbWVzdGFtcCI6ICIyMDI0LTA2LTA0VDA2OjA0OjAwIn0=.a1b2c3d4e5f6...",
  "pin": "1234"
}
```

**Processing:**
```
1. Verify JWT in cookie
   └─ Extract user_id, role
   
2. Validate role == 'student'
   └─ Reject if not student
   
3. Parse request body
   ├─ Extract token
   └─ Extract PIN
   
4. Verify QR token
   ├─ Decode Base64
   ├─ Verify HMAC signature
   ├─ Check timestamp (< 30s)
   └─ Extract session_id
   
5. Fetch session from DB
   ├─ Check status == 'active'
   └─ Verify PIN matches
   
6. Check enrollment
   └─ Verify student in unit
   
7. Check duplicate
   └─ Verify not already marked
   
8. Insert attendance record
   ├─ Record marked_at timestamp
   └─ Set status = 'present'
   
9. Push SSE update
   └─ Notify lecturer's live view
   
10. Return success response
```

**Response:**
```json
{
  "success": true,
  "message": "Attendance marked successfully",
  "session_id": 1
}
```

---

## Security Architecture

### Authentication Layer
- **JWT**: Stateless, time-limited tokens
- **Bcrypt**: Password hashing with salt
- **HttpOnly Cookies**: Prevents XSS access
- **SameSite=Strict**: CSRF protection

### Authorization Layer
- **Role-Based Access Control**: Student, Lecturer, Admin
- **Decorator Pattern**: `@role_required('student')`
- **Server-Side Enforcement**: Never trust client
- **Audit Logging**: All actions logged with user + IP

### Data Protection
- **Parameterized Queries**: Prevents SQL injection
- **Input Validation**: Server-side only
- **HMAC Signing**: QR tokens cryptographically signed
- **Rate Limiting**: Login endpoint protected

### Network Security
- **HTTPS/SSL**: Encrypted transport (production)
- **CORS**: Same-origin only
- **CSRF Tokens**: Session validation
- **Security Headers**: Strict-Transport-Security, etc.

---

## Scalability Considerations

### Database Optimization
- Foreign key constraints for referential integrity
- Proper indexing on frequently queried columns
- Connection pooling for concurrent requests
- Prepared statements for query efficiency

### API Optimization
- Pagination for large datasets
- Caching for frequently accessed data
- Lazy loading for related entities
- Compression for responses

### Frontend Optimization
- Minified CSS/JS in production
- Lazy loading for images
- Efficient DOM manipulation
- Event delegation for dynamic content

### Deployment Optimization
- Gunicorn with multiple workers
- Nginx as reverse proxy
- Load balancing for multiple instances
- Database replication for high availability

---

## Error Handling

**Consistent Error Response Format:**
```json
{
  "success": false,
  "error": "Human-readable error message"
}
```

**HTTP Status Codes:**
- 200: Success
- 201: Created
- 400: Bad request (validation error)
- 401: Unauthorized (authentication failed)
- 403: Forbidden (authorization failed)
- 404: Not found
- 500: Server error

**Error Handling Strategy:**
1. Validate input at API boundary
2. Check permissions before processing
3. Verify database state before mutations
4. Log errors with context
5. Return user-friendly messages
6. Never expose internal details

---

## Testing Strategy

### Unit Tests
- Authentication flows
- QR token generation/verification
- Attendance validation logic
- Database model operations

### Integration Tests
- Complete attendance marking flow
- Session lifecycle (create → close)
- User management workflows
- Role-based access control

### End-to-End Tests
- Student registration → attendance marking
- Lecturer session → attendance export
- Admin user management → reporting

### Security Tests
- SQL injection attempts
- XSS payload handling
- CSRF token validation
- Rate limiting enforcement

---

## Deployment Architecture

**Development:**
```
Flask Development Server (Port 5000)
    ↓
SQLite/MySQL (Local)
```

**Production:**
```
┌─────────────────────────────────────┐
│  Client Browser (HTTPS)             │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Nginx (Reverse Proxy + SSL)        │
│  - Load balancing                   │
│  - Static file serving              │
│  - Compression                      │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Gunicorn (WSGI Server)             │
│  - Multiple workers                 │
│  - Process management               │
│  - Request handling                 │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Flask Application                  │
│  - Business logic                   │
│  - API endpoints                    │
│  - Authentication                   │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  MySQL/PostgreSQL (Production DB)   │
│  - Replication                      │
│  - Backups                          │
│  - Connection pooling               │
└─────────────────────────────────────┘
```

---

## Performance Metrics

- **API Response Time**: < 200ms (p95)
- **Database Query Time**: < 100ms (p95)
- **Page Load Time**: < 2s (full page)
- **QR Scan Time**: < 1s (decode)
- **Concurrent Users**: 1000+ (with proper scaling)

---

## Future Enhancements

1. **Microservices**: Separate auth, attendance, reporting services
2. **Caching**: Redis for session data and frequently accessed records
3. **Message Queue**: RabbitMQ for async tasks (exports, notifications)
4. **Search**: Elasticsearch for advanced reporting queries
5. **Mobile App**: Native iOS/Android applications
6. **Biometrics**: Fingerprint/face recognition integration
7. **Analytics**: Advanced dashboards with predictive analytics
8. **Multi-tenancy**: Support multiple institutions

---

This architecture ensures the system is:
- **Secure**: Multiple layers of protection
- **Scalable**: Designed for growth
- **Maintainable**: Clear separation of concerns
- **Testable**: Comprehensive test coverage
- **Production-Ready**: Enterprise-grade implementation

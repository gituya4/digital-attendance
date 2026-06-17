CREATE DATABASE IF NOT EXISTS attendance_db;
USE attendance_db;

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('student', 'lecturer', 'admin') NOT NULL,
    registration_number VARCHAR(50),
    staff_id VARCHAR(50),
    department VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
);

CREATE TABLE units (
    unit_id INT PRIMARY KEY AUTO_INCREMENT,
    unit_code VARCHAR(20) UNIQUE NOT NULL,
    unit_name VARCHAR(150) NOT NULL,
    department VARCHAR(100),
    semester VARCHAR(20),
    academic_year VARCHAR(10),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_code (unit_code)
);

CREATE TABLE lecturer_units (
    id INT PRIMARY KEY AUTO_INCREMENT,
    lecturer_id INT NOT NULL,
    unit_id INT NOT NULL,
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (lecturer_id, unit_id),
    FOREIGN KEY (lecturer_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (unit_id) REFERENCES units(unit_id) ON DELETE CASCADE,
    INDEX idx_lecturer (lecturer_id),
    INDEX idx_unit (unit_id)
);

CREATE TABLE enrollments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    unit_id INT NOT NULL,
    enrolled_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (student_id, unit_id),
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (unit_id) REFERENCES units(unit_id) ON DELETE CASCADE,
    INDEX idx_student (student_id),
    INDEX idx_unit (unit_id)
);

CREATE TABLE sessions (
    session_id INT PRIMARY KEY AUTO_INCREMENT,
    unit_id INT NOT NULL,
    lecturer_id INT NOT NULL,
    session_pin CHAR(4) NOT NULL,
    current_token VARCHAR(512),
    token_generated_at DATETIME,
    status ENUM('active', 'closed') DEFAULT 'active',
    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    end_time DATETIME,
    session_notes TEXT,
    FOREIGN KEY (unit_id) REFERENCES units(unit_id) ON DELETE CASCADE,
    FOREIGN KEY (lecturer_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_unit (unit_id),
    INDEX idx_lecturer (lecturer_id),
    INDEX idx_status (status),
    INDEX idx_start_time (start_time)
);

CREATE TABLE attendance_records (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    session_id INT NOT NULL,
    student_id INT NOT NULL,
    unit_id INT NOT NULL,
    marked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('present', 'manual') DEFAULT 'present',
    UNIQUE (session_id, student_id),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (unit_id) REFERENCES units(unit_id) ON DELETE CASCADE,
    INDEX idx_session (session_id),
    INDEX idx_student (student_id),
    INDEX idx_unit (unit_id),
    INDEX idx_marked_at (marked_at)
);

CREATE TABLE correction_requests (
    request_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    session_id INT NOT NULL,
    reason TEXT NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    admin_comment TEXT,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reviewed_at DATETIME,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
    INDEX idx_student (student_id),
    INDEX idx_status (status),
    INDEX idx_submitted_at (submitted_at)
);

CREATE TABLE audit_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    detail TEXT,
    ip_address VARCHAR(45),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_user (user_id),
    INDEX idx_action (action),
    INDEX idx_timestamp (timestamp)

CREATE TABLE notifications (
    notification_id INT PRIMARY KEY AUTO_INCREMENT,
    from_user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    to_user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    unit_id INT REFERENCES units(unit_id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'absence_warning',
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_to_user (to_user_id),
    INDEX idx_is_read (is_read),
    INDEX idx_created_at (created_at)
);
);

#!/usr/bin/env python3
"""
Database Connection Test & User Creation Script
Tests MySQL connection and creates test users for each role
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.models.user import User
from app.models.unit import Unit
from app.database import db

def test_database_connection():
    """Test if database connection works"""
    print("\n" + "="*70)
    print("TESTING DATABASE CONNECTION")
    print("="*70)
    
    try:
        with db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"✅ MySQL Connection Successful!")
                print(f"   MySQL Version: {version}")
        return True
    except Exception as e:
        print(f"❌ Database Connection Failed!")
        print(f"   Error: {e}")
        return False

def create_test_users():
    """Create test users for each role"""
    print("\n" + "="*70)
    print("CREATING TEST USERS")
    print("="*70)
    
    test_users = [
        {
            'name': 'Alice Johnson',
            'email': 'alice@example.com',
            'password': 'TestPassword123',
            'role': 'student',
            'registration_number': 'CS/MK/0792/09/23'
        },
        {
            'name': 'Bob Smith',
            'email': 'bob@example.com',
            'password': 'TestPassword123',
            'role': 'student',
            'registration_number': 'CS/MK/0793/09/23'
        },
        {
            'name': 'Dr. Sarah Williams',
            'email': 'sarah@example.com',
            'password': 'TestPassword123',
            'role': 'lecturer',
            'staff_id': 'LEC001',
            'department': 'Computer Science'
        },
        {
            'name': 'Prof. James Brown',
            'email': 'james@example.com',
            'password': 'TestPassword123',
            'role': 'lecturer',
            'staff_id': 'LEC002',
            'department': 'Information Technology'
        },
        {
            'name': 'Admin User',
            'email': 'admin@example.com',
            'password': 'TestPassword123',
            'role': 'admin'
        }
    ]
    
    created_count = 0
    failed_count = 0
    
    for user_data in test_users:
        try:
            if user_data['role'] == 'student':
                result = User.create(
                    user_data['name'],
                    user_data['email'],
                    user_data['password'],
                    user_data['role'],
                    registration_number=user_data['registration_number']
                )
            elif user_data['role'] == 'lecturer':
                result = User.create(
                    user_data['name'],
                    user_data['email'],
                    user_data['password'],
                    user_data['role'],
                    staff_id=user_data['staff_id'],
                    department=user_data['department']
                )
            else:  # admin
                result = User.create(
                    user_data['name'],
                    user_data['email'],
                    user_data['password'],
                    user_data['role']
                )
            
            if result:
                print(f"✅ Created {user_data['role'].upper()}: {user_data['name']}")
                print(f"   Email: {user_data['email']}")
                if user_data['role'] == 'student':
                    print(f"   Reg #: {user_data['registration_number']}")
                elif user_data['role'] == 'lecturer':
                    print(f"   Staff ID: {user_data['staff_id']}")
                print()
                created_count += 1
            else:
                print(f"❌ Failed to create {user_data['role']}: {user_data['name']}")
                failed_count += 1
        except Exception as e:
            print(f"❌ Error creating {user_data['role']}: {user_data['name']}")
            print(f"   Error: {e}")
            failed_count += 1
    
    return created_count, failed_count

def verify_users():
    """Verify users were created"""
    print("\n" + "="*70)
    print("VERIFYING CREATED USERS")
    print("="*70)
    
    try:
        query = "SELECT user_id, full_name, email, role FROM users ORDER BY user_id"
        users = db.execute_query(query)
        
        if users:
            print(f"\n✅ Found {len(users)} users in database:\n")
            for user in users:
                print(f"   ID: {user['user_id']}")
                print(f"   Name: {user['full_name']}")
                print(f"   Email: {user['email']}")
                print(f"   Role: {user['role'].upper()}")
                print()
            return True
        else:
            print("❌ No users found in database")
            return False
    except Exception as e:
        print(f"❌ Error verifying users: {e}")
        return False

def create_test_units():
    """Create test units"""
    print("\n" + "="*70)
    print("CREATING TEST UNITS")
    print("="*70)
    
    test_units = [
        {
            'code': 'CS101',
            'name': 'Introduction to Computer Science',
            'department': 'Computer Science',
            'semester': '1',
            'year': '2024'
        },
        {
            'code': 'CS102',
            'name': 'Data Structures',
            'department': 'Computer Science',
            'semester': '1',
            'year': '2024'
        },
        {
            'code': 'IT101',
            'name': 'Network Fundamentals',
            'department': 'Information Technology',
            'semester': '1',
            'year': '2024'
        }
    ]
    
    created_count = 0
    
    for unit_data in test_units:
        try:
            result = Unit.create(
                unit_data['code'],
                unit_data['name'],
                unit_data['department'],
                unit_data['semester'],
                unit_data['year']
            )
            
            if result:
                print(f"✅ Created Unit: {unit_data['code']} - {unit_data['name']}")
                created_count += 1
        except Exception as e:
            print(f"❌ Error creating unit {unit_data['code']}: {e}")
    
    return created_count

def verify_units():
    """Verify units were created"""
    print("\n" + "="*70)
    print("VERIFYING CREATED UNITS")
    print("="*70)
    
    try:
        query = "SELECT unit_id, unit_code, unit_name, department FROM units ORDER BY unit_id"
        units = db.execute_query(query)
        
        if units:
            print(f"\n✅ Found {len(units)} units in database:\n")
            for unit in units:
                print(f"   ID: {unit['unit_id']}")
                print(f"   Code: {unit['unit_code']}")
                print(f"   Name: {unit['unit_name']}")
                print(f"   Department: {unit['department']}")
                print()
            return True
        else:
            print("❌ No units found in database")
            return False
    except Exception as e:
        print(f"❌ Error verifying units: {e}")
        return False

def test_login():
    """Test login with created users"""
    print("\n" + "="*70)
    print("TESTING LOGIN FUNCTIONALITY")
    print("="*70)
    
    test_logins = [
        ('alice@example.com', 'TestPassword123', 'Student'),
        ('sarah@example.com', 'TestPassword123', 'Lecturer'),
        ('admin@example.com', 'TestPassword123', 'Admin')
    ]
    
    from app.services.auth_service import AuthService
    
    for email, password, role in test_logins:
        try:
            success, user_data, message = AuthService.login(email, password)
            if success:
                print(f"✅ {role} Login Successful: {user_data['full_name']}")
            else:
                print(f"❌ {role} Login Failed: {message}")
        except Exception as e:
            print(f"❌ Error testing {role} login: {e}")

def main():
    """Main test function"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  DIGITAL ATTENDANCE SYSTEM - DATABASE TEST & SETUP".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    # Test database connection
    if not test_database_connection():
        print("\n❌ Cannot proceed without database connection")
        sys.exit(1)
    
    # Create test users
    created, failed = create_test_users()
    print(f"\n📊 User Creation Summary: {created} created, {failed} failed")
    
    # Verify users
    verify_users()
    
    # Create test units
    units_created = create_test_units()
    print(f"\n📊 Unit Creation Summary: {units_created} units created")
    
    # Verify units
    verify_units()
    
    # Test login
    test_login()
    
    # Final summary
    print("\n" + "="*70)
    print("SETUP COMPLETE")
    print("="*70)
    print("\n✅ Database is ready for testing!")
    print("\nTest Accounts:")
    print("  Student 1: alice@example.com / TestPassword123")
    print("  Student 2: bob@example.com / TestPassword123")
    print("  Lecturer 1: sarah@example.com / TestPassword123")
    print("  Lecturer 2: james@example.com / TestPassword123")
    print("  Admin: admin@example.com / TestPassword123")
    print("\nNext Steps:")
    print("  1. Start the application: python run.py")
    print("  2. Visit: http://localhost:5000")
    print("  3. Login with test accounts above")
    print("  4. Test workflows (student, lecturer, admin)")
    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    main()

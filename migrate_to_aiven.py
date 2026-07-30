#!/usr/bin/env python3
"""
Migrate data from local MySQL to Aiven
Run this before switching to Aiven in production
"""
import os
import sys
from dotenv import load_dotenv
from app.database import Database

load_dotenv()

# Local database configuration
local_db = Database()
local_db.host = 'localhost'
local_db.user = 'root'
local_db.password = 'Root@1234'
local_db.database = 'attendance_db'
local_db.port = 3306

# Aiven database configuration (from .env)
aiven_db = Database()

def migrate_table(table_name):
    """Migrate all data from a table"""
    print(f"Migrating {table_name}...")
    
    try:
        # Get data from local database
        local_db.database = 'attendance_db'
        data = local_db.execute_query(f"SELECT * FROM {table_name}")
        
        if not data:
            print(f"  No data in {table_name}")
            return
        
        print(f"  Found {len(data)} records")
        
        # Clear destination table
        aiven_db.execute_query(f"DELETE FROM {table_name}")
        print(f"  Cleared destination table")
        
        # Insert data into Aiven
        if data:
            columns = list(data[0].keys())
            placeholders = ', '.join(['%s'] * len(columns))
            columns_str = ', '.join(columns)
            
            values = []
            for row in data:
                values.append(tuple(row[col] for col in columns))
            
            aiven_db.execute_many(
                f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})",
                values
            )
            print(f"  ✅ Migrated {len(data)} records")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")

def main():
    print("Starting migration from local MySQL to Aiven...")
    print(f"Local DB: localhost/attendance_db")
    print(f"Aiven DB: {aiven_db.host}/{aiven_db.database}")
    print()
    
    tables = [
        'users',
        'units',
        'lecturer_units',
        'enrollments',
        'sessions',
        'attendance_records',
        'correction_requests',
        'audit_log',
        'notifications'
    ]
    
    for table in tables:
        migrate_table(table)
        print()
    
    print("Migration complete!")

if __name__ == '__main__':
    main()

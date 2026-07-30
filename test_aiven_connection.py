#!/usr/bin/env python3
"""Test script to verify Aiven database connection"""
import os
from dotenv import load_dotenv
from app.database import db

load_dotenv()

print("Testing Aiven Database Connection...")
print(f"Host: {os.getenv('DB_HOST')}")
print(f"Port: {os.getenv('DB_PORT')}")
print(f"Database: {os.getenv('DB_NAME')}")
print(f"User: {os.getenv('DB_USER')}")
print(f"SSL: {os.getenv('DB_SSL')}")
print()

try:
    # Test connection with a simple query
    result = db.execute_query("SELECT 1 as test", fetch_one=True)
    print("✅ Database connection successful!")
    print(f"Test query result: {result}")
    
    # Check if tables exist
    tables = db.execute_query("SHOW TABLES")
    print(f"\n✅ Found {len(tables)} tables:")
    for table in tables:
        print(f"  - {list(table.values())[0]}")
    
except Exception as e:
    print(f"❌ Database connection failed!")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

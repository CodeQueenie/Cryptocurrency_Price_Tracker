#!/usr/bin/env python3
"""
Update Database Password
-----------------------
A simple utility to update the database password in the .env file.
"""

import os
from dotenv import load_dotenv, set_key

# Load current environment variables
load_dotenv()

print("Current database settings:")
print(f"DB_TYPE: {os.getenv('DB_TYPE', 'Not set')}")
print(f"DB_HOST: {os.getenv('DB_HOST', 'Not set')}")
print(f"DB_PORT: {os.getenv('DB_PORT', 'Not set')}")
print(f"DB_NAME: {os.getenv('DB_NAME', 'Not set')}")
print(f"DB_USER: {os.getenv('DB_USER', 'Not set')}")
print(f"DB_PASSWORD: {'*****' if os.getenv('DB_PASSWORD') else 'Not set'}")
print()

# Get new password
new_password = input("Enter your PostgreSQL password for user 'postgres': ")

# Update the .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
set_key(env_path, "DB_PASSWORD", new_password)

print("\nPassword updated successfully!")
print("Please restart the application to use the new password.")

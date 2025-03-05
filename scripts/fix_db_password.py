#!/usr/bin/env python3
"""
Fix Database Password
--------------------
A simple utility to fix the database password in the .env file by removing quotes.
"""

import os
import re
from dotenv import load_dotenv

# Load current environment variables
load_dotenv()

# Get the current .env file path
env_path = os.path.join(os.path.dirname(__file__), '.env')

# Read the current .env file
with open(env_path, 'r') as f:
    env_content = f.read()

# Find and fix the DB_PASSWORD line
password_pattern = r'DB_PASSWORD\s*=\s*["\'](.+?)["\'](.*)'
password_match = re.search(password_pattern, env_content)

if password_match:
    password_value = password_match.group(1)
    comment = password_match.group(2) or ''
    
    # Replace the line with a version without quotes
    old_line = f'DB_PASSWORD="{password_value}"{comment}'
    new_line = f'DB_PASSWORD={password_value}{comment}'
    
    env_content = env_content.replace(old_line, new_line)
    
    # Write the updated content back to the .env file
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print("Fixed DB_PASSWORD in .env file by removing quotes.")
else:
    print("No quoted DB_PASSWORD found in .env file.")

print("\nPlease restart the application to use the updated password format.")

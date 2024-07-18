import sys
from app import app, db, register_admin

if len(sys.argv) != 3:
    print("Usage: python register_admin.py <username> <password>")
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]

with app.app_context():
    register_admin(username, password)
    print(f"Admin {username} registered successfully!")

import sys
from flask import Flask
from database import db, delete_user_by_email

if len(sys.argv) != 2:
    print("Usage: python delete_user.py <email>")
    sys.exit(1)

email = sys.argv[1]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/users.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

confirm = input(f"Are you sure you want to delete the user with email {email}? (y/n): ")
if confirm.lower() != 'y':
    print("Operation cancelled.")
    sys.exit(0)

if delete_user_by_email(app, email):
    print(f"User with email {email} has been deleted.")
else:
    print(f"No user found with email {email}.")

from models import db, Admin
from app import app

db.drop_all()
db.create_all()

print("Enter your Admin Username:")
username = input()

print("Enter your Password:")
raw_pass = input()

print("Enter your password again:")
raw_conf_pass = input()

if not username or not raw_pass or not raw_conf_pass:
    print("Input Error")
else:
    pwd = Admin.hash_pwd(raw_pass)

    admin = Admin(username=username, password=pwd)
    db.session.add(admin)
    try:
        db.session.commit()
        print("Admin saved to database.")
    except:
        db.session.rollback()
        print("Error saving Admin to database.")

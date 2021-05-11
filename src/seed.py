from models import db, Admin
from app import app

db.drop_all()
db.create_all()

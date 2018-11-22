from app import app
from db import db

db.init_app(app)


 #To create the tables using sqlalchemy, and not use the script create_tables.py. Use the following.
@app.before_first_request
def create_tables():
	db.create_all()


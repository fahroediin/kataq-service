# kataq/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

db = SQLAlchemy()
admin = Admin(name='KataQ Dashboard')
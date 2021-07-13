from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

from config import app

db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('kategoriya nomi', db.String(255))

class News(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    title = db.Column('Sarlavha', db.String(255))
    content = db.Column('Mazmuni', db.Text)
    datetime = db.Column('Sana', db.DateTime, default=datetime.now)
    views = db.Column("Ko'rishlar soni", db.Integer, default=0)
    is_published = db.Column("Chop etilishi", db.Boolean)
    photo = db.Column("Muqova rasmi", db.String(255))

    cat_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)

class User(UserMixin, db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    fullname = db.Column("To'liq ism", db.String(255))
    username = db.Column("Login", db.String(255), unique=True)
    password = db.Column("Parol", db.String(255))


if __name__ == "__main__":
    db.create_all()
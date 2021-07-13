from flask import Flask
from pathlib import Path
import os
from flask_login import LoginManager


OS_UPLOAD_PATH = os.path.join("static", "uploads", "images")

IMAGE_UPLOAD_DIR = Path(OS_UPLOAD_PATH)
if not IMAGE_UPLOAD_DIR.exists():
    os.makedirs(OS_UPLOAD_PATH)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = b"d1s5d1s5d56asd1"

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = u"Iltimos shaxsiy kabinetingizga kiring"
login_manager.login_message_category = "warning"
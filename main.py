from config import app, login_manager
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first_or_404()

from main_page_view import *
from category_view import *
from errors import *
from admin_page_view import *
from add_person import *
from contex import *


if __name__ == "__main__":
    app.run(debug=True)
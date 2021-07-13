from flask import render_template, request, session
from config import app
from models import Category,db
from flask_login import login_required

@app.route("/admin/create_category/", methods=["GET", "POST"])
@login_required
def add_category_view():

    category_name = request.form.get("category_name", None)
    
    if category_name:
        c = Category(name=category_name)
        db.session.add(c)
        db.session.commit()

    return render_template("admin/add_category.html")

# @app.route("/admin/change_category/", methods=["GET", "POST"])
# def change_category_view():
#     # category_name = request.form.get("category_name", None)
#     return render_template("admin/change_category.html")
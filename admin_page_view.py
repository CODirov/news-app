from flask import render_template, request, redirect, url_for, session
from flask.helpers import flash
from config import app, OS_UPLOAD_PATH
from models import News, db, User
from uuid import uuid4
import os
import bcrypt
from flask_login import login_user, login_required, logout_user

@app.route("/admin/admin_page/")
@login_required
def admin_page_view():

    if ("action" and "_id") in request.args:
        try:
            _id = int(request.args.get("_id"))
        except:
            return redirect(url_for('admin_page_view'))

        if request.args.get("action")=="make_active":
            choosen_item = News.query.filter_by(id=_id).first_or_404()
            choosen_item.is_published = True
            db.session.commit()

        elif request.args.get("action")=="make_inactive":
            choosen_item = News.query.filter_by(id=_id).first_or_404()
            choosen_item.is_published = False
            db.session.commit()

        elif request.args.get("action")=="delete":
            choosen_item = News.query.filter_by(id=_id).first_or_404()
            try:
                os.unlink(os.path.join("static", "uploads", "images", choosen_item.photo))
            except:
                pass
            db.session.delete(choosen_item)            
            db.session.commit()
            return redirect(url_for('admin_page_view'))

        else:
            return redirect(url_for('admin_page_view'))
            
        
    home_page = News.query.order_by(News.id.desc()).all()
    return render_template("admin/admin_page.html", all_pages = home_page)

@app.route("/admin/admin_page/<int:_id>/", methods=["GET", "POST"])
@login_required
def update_view(_id):
    
    if request.method == 'POST':
        news = News.query.filter_by(id=_id).first_or_404()

        news.title = request.form["person_title"]
        news.content = request.form["person_content"]
        news.is_published = bool(request.form.get("publish_status", False))

        try:
            news.cat_id = int(request.form.get("category_id"))

        except:
            return redirect(url_for('update_view', _id=_id))

        if "person's photo" in request.files:
            persons_photo = request.files["person's photo"]
            photo_filename = str(uuid4())+"."+persons_photo.filename.split(".")[-1]
            persons_photo.save(os.path.join(OS_UPLOAD_PATH, photo_filename))

            if persons_photo.filename.split(".")[-1] != "":
                news.photo=photo_filename

        db.session.commit()
        return redirect(url_for('admin_page_view'))
    elif request.method == 'GET':
        if request.args.get("action", None)=="delete-thumb":
            chosen_item = News.query.filter_by(id=_id).first_or_404()
            os.unlink(os.path.join("static", "uploads", "images", chosen_item.photo))
            chosen_item.photo = ""
            db.session.commit()
            return redirect(url_for('update_view', _id=_id))

        chosen_item = News.query.filter_by(id=_id).first_or_404()
        return render_template("admin/update_person_info.html", item=chosen_item)


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", None)
    
        if not username or not password:
            flash("Iltimos, login va parolni tog'ri kiriting!", "warning")

        else:
            user = User.query.filter_by(username=username.strip()).first_or_404()
            if bcrypt.checkpw(password.encode(), user.password):
                flash("siz kabinetingizga kirdingiz", "success")
                session["login"] = username
                session["password"] = password.strip()
                login_user(user)
                return redirect(url_for("admin_page_view"))
            else:
                flash("parol xato", "danger")
    
    return render_template("admin/login.html")


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form.get("fullname", None)
        username = request.form.get("username", None)
        password1 = request.form.get("password1", None)
        password2 = request.form.get("password2", None)

        if not username:
            flash("username kiritilmadi!", "danger")
            return render_template("admin/register.html")
        
        if not password1 or not password2:
            flash("parolni to'g'ri kiriting", "danger")
            return render_template("admin/register.html")

        elif password1 and password2 and password1.strip() != password2.strip():
            flash("Parollar mos kelmayapti!", "danger")
            return render_template("admin/register.html")

        else:
            user = User()
            user.username = username
            if fullname:
                user.fullname = fullname
                user.password = bcrypt.hashpw(password1.strip().encode(), bcrypt.gensalt())
                db.session.add(user)
                db.session.commit()
                flash("Siz ro'yhatdan o'tdingiz!", "success")
            return render_template("admin/register.html")

    return render_template("admin/register.html")

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("login"))
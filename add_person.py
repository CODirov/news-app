import os
from datetime import datetime
from flask import render_template, request, url_for, session
from werkzeug.utils import redirect
from models import News, db
from uuid import uuid4
from config import app, OS_UPLOAD_PATH
from flask_login import login_required

@app.route("/admin/create/", methods=["GET", "POST"])
@login_required
def add_person():
    
    if request.method == "POST":
        news = News()

        news.title = request.form["person_title"]
        news.content = request.form["person_content"]
        news.is_published = bool(request.form.get("publish_status", False))

        try:
            news.cat_id = int(request.form.get("category_id"))

        except:
            return redirect(url_for('add_person'))

        if "person's photo" in request.files:
            persons_photo = request.files["person's photo"]
            photo_filename = str(uuid4())+"."+persons_photo.filename.split(".")[-1]
            persons_photo.save(os.path.join(OS_UPLOAD_PATH, photo_filename))

            if persons_photo.filename.split(".")[-1] != "":
                news.photo=photo_filename

        db.session.add(news)
        db.session.commit()

        return redirect(url_for('add_person'))


    return render_template('admin/add_person.html')

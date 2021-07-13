from flask import render_template, request
from models import Category, News, db
from utils.search import highlight_words
from config import app


@app.route("/")
def home_page_view():
    cats = Category.query.all()
    term=request.args.get("term",None)
    cat_id=request.args.get("category",None)

    if term:
        home_page=News.query.filter(News.title.contains(term) | News.content.contains(term)).all()
        temp=[]
        for single_page in home_page:
            single_page.title=highlight_words(single_page.title,term,"<span style='background-color: yellow;'>","</span>")

            single_page.content=highlight_words(single_page.content,term,"<span style='background-color: yellow;'>","</span>")
            temp.append(single_page)
        home_page=temp
    elif cat_id:
        home_page = News.query.filter_by(cat_id=int(cat_id)).all()
    else:
        home_page=News.query.all()

    return render_template("client/home_page.html", pages_view = home_page, qidirilgan_soz = term, kategoriyalar=cats)


@app.route("/<int:_id>/")
def single_page_view(_id):
    single_page = News.query.filter_by(id=str(_id)).first_or_404()
    if single_page.views is None:
        single_page.views=0
    single_page.views = single_page.views+1
    db.session.commit()
    
    return render_template("client/single_page.html", page = single_page)
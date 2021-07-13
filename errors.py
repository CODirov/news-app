from flask import render_template
from config import app

@app.errorhandler(404)
@app.errorhandler(500)
def page_404_view(e):
    return render_template("client/404.html")
from config import app
from models import Category


@app.context_processor
def category_contex_manager():
    cats = Category.query.all()
    return{"kategoriyalar": cats}
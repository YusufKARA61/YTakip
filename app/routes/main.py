# app/routes/main.py
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('frontend/home.html')

# Diğer route'larınız buraya eklenecek

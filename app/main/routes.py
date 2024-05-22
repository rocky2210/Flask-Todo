from flask import Blueprint, render_template, redirect, url_for
from app.main import bp


@bp.route('/')
def index():
    return render_template('main/index.html')

@bp.route('/about')
def about():
    return render_template('main/about.html')

@bp.route('/faq')
def faq():
    return render_template('main/FAQs.html')



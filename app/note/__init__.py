from flask import Blueprint

bp = Blueprint('note', __name__)

from app.note import routes

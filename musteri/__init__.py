from flask import Blueprint

musteri_bp = Blueprint("musteri", __name__)

from . import routes
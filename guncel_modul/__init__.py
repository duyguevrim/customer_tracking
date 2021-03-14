from flask import Blueprint

guncel_modul = Blueprint("guncel_modul", __name__)

from . import routes
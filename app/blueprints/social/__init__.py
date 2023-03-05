from flask import Blueprint
bp = Blueprint('social', __name__, url_prefix='/social')
from . import routes, models
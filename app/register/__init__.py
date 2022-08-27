from flask import Blueprint, current_app
register = Blueprint('register', __name__)
from . import views, errors

@register.app_context_processor
def global_variables():
    return dict(app_name = current_app.config['ORGANISATION_NAME'])

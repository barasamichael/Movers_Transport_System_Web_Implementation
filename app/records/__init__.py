from flask import Blueprint, current_app
records = Blueprint('records', __name__)
from . import views, errors

@records.app_context_processor
def global_variables():
    return dict(app_name = current_app.config['ORGANISATION_NAME'])

from flask import Blueprint, current_app
profiles = Blueprint('profiles', __name__)
from . import views, errors
from ..models import Permission 

@profiles.app_context_processor
def global_variables():
    return dict(app_name = current_app.config['ORGANISATION_NAME'], 
            Permission = Permission)

from flask import render_template
from . import authentication

@authentication.app_errorhandler(404)
def page_not_found(e):
    return render_template('authentication/404.html'), 404


@authentication.app_errorhandler(500)
def internal_server_error(e):
    return render_template('authentication/500.html'), 500

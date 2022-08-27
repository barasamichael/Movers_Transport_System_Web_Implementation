from flask import render_template
from . import records


@records.app_errorhandler(403)
def forbidden(e):
    return render_template('records/403.html'), 403


@records.app_errorhandler(404)
def page_not_found(e):
    return render_template('records/404.html'), 404


@records.app_errorhandler(500)
def internal_server_error(e):
    return render_template('records/500.html'), 500

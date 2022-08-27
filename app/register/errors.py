from flask import render_template
from . import register


@register.app_errorhandler(403)
def forbidden(e):
    return render_template('register/403.html'), 403


@register.app_errorhandler(404)
def page_not_found(e):
    return render_template('register/404.html'), 404


@register.app_errorhandler(500)
def internal_server_error(e):
    return render_template('register/500.html'), 500

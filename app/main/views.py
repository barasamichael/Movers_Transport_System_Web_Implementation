import flask
from . import main
from .. import db
from ..models import vehicle_make


@main.route('/')
@main.route('/home')
@main.route('/homepage')
def homepage():
    vehicle_makes = vehicle_make.query.all()
    return flask.render_template('main/homepage.html', \
            vehicle_makes = vehicle_makes)

import flask, flask_login
from . import records
from .. import db
from ..models import (small_scale_farmer, loader, driver, offence, good, vehicle, 
        vehicle_make, offender, member, service, order, trip)


@records.route('/list_of_members')
@flask_login.login_required
def list_of_members():
    members = member.query.all()
    return flask.render_template('records/list_of_members.html', \
            members = members)


@records.route('/list_of_small_scale_farmers')
@flask_login.login_required
def list_of_small_scale_farmers():
    farmers = small_scale_farmer.query\
            .join(member, member.member_id == small_scale_farmer.group_id)\
            .add_columns(
                    small_scale_farmer.farmer_id,
                    small_scale_farmer.first_name,
                    small_scale_farmer.last_name,
                    small_scale_farmer.middle_name,
                    small_scale_farmer.gender,
                    small_scale_farmer.email_address,
                    member.name
                    ).order_by(member.name.asc()).all()

    return flask.render_template('records/list_of_small_scale_farmers.html', \
            farmers = farmers)

@records.route('/list_of_drivers')
@flask_login.login_required
def list_of_drivers():
    drivers = driver.query.all()
    return flask.render_template('records/list_of_drivers.html', \
            drivers = drivers)


@records.route('/list_of_loaders')
@flask_login.login_required
def list_of_loaders():
    loaders = loader.query.all()
    return flask.render_template('records/list_of_loaders.html', \
            loaders = loaders)


@records.route('/list_of_goods')
@flask_login.login_required
def list_of_goods():
    goods = good.query.all()
    return flask.render_template('records/list_of_goods.html', \
            goods = goods)


@records.route('/list_of_offences')
@flask_login.login_required
def list_of_offences():
    offences = offence.query.all()
    return flask.render_template('records/list_of_offences.html', \
            offences = offences)

@records.route('/list_of_vehicles')
@flask_login.login_required
def list_of_vehicles():
    vehicles = vehicle.query\
    .join(vehicle_make, vehicle.make_id == vehicle_make.make_id)\
    .add_columns(
            vehicle.vehicle_id,
            vehicle.plate_no,
            vehicle_make.make_type
            )\
    .all()

    return flask.render_template('records/list_of_vehicles.html', \
            vehicles = vehicles)

@records.route('/list_of_fired_drivers')
@flask_login.login_required
def list_of_fired_drivers():
    drivers = driver.query.all()
    return flask.render_template('records/list_of_fired_drivers.html', \
            drivers = drivers)


@records.route('/list_of_surcharged_drivers')
@flask_login.login_required
def list_of_surcharged_drivers():
    drivers = driver.query.all()
    return flask.render_template('records/list_of_surcharged_drivers.html', \
            drivers = drivers)


@records.route('/list_of_suspended_drivers')
@flask_login.login_required
def list_of_suspended_drivers():
    drivers = driver.query.all()
    return flask.render_template('records/list_of_suspended_drivers.html', \
            drivers = drivers)


@records.route('/list_of_offenders')
@flask_login.login_required
def list_of_offenders():
    offenders = driver.query.all()

    return flask.render_template('records/list_of_offenders.html', \
            offenders = offenders)


@records.route('/list_of_vehicle_makes')
@flask_login.login_required
def list_of_vehicle_makes():
    vehicle_makes = vehicle_make.query.all()

    return flask.render_template('records/list_of_vehicle_makes.html', \
            vehicle_makes = vehicle_makes)

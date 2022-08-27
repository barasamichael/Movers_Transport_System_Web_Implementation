import flask, flask_login
from . import register
from .forms import (Vehicle_Make_Form, Small_Scale_Farmer_Form, Driver_Form, 
        Loader_Form, Offence_Form, Good_Form, Trip_Form, Order_Form, 
        Offender_Form, Vehicle_Form)
from .. import db
from ..models import (vehicle_make, small_scale_farmer, driver, loader, offence, 
        good, vehicle, trip
        )

from sqlalchemy.exc import IntegrityError


@register.route('/user/register_trip/<int:user_id>', methods = ['GET', 'POST'])
@flask_login.login_required
def register_trip(user_id):
    vehicles = [(item.vehicle_id, item.plate_no) for item in vehicle.query\
            .order_by(vehicle.plate_no.desc()).all()]

    drivers= [(item.driver_id, item.first_name + " " + item.middle_name) \
            for item in driver.query.order_by(driver.first_name.desc()).all()]


    form = Trip_Form()

    form.vehicle_id.choices = vehicles
    form.driver_id.choices = drivers

    if form.validate_on_submit():
        t_trip = trip(
                trip_date = form.trip_date.data,
                driver_id = form.driver_id.data,
                vehicle_id = form.vehicle_id.data,
                distance = form.distance.data
                )
        try:
            db.session.add(t_trip)
            db.session.commit()

            flask.flash('Trip made successfully.')
            return flask.redirect(flask.url_for('profiles.user_view_trips', 
                user_id = user_id))

        except IntegrityError:
            db.session.rollback()
            flask.flash('The values you entered are invalid or already exist.')

        except SyntaxError:
            flask.flash('An error occurred while saving the data.')

    return flask.render_template('register/register_trip.html', form = form)


@register.route('/register_vehicle_make', methods = ['GET', 'POST'])
@flask_login.login_required
def register_vehicle_make():
    form = Vehicle_Make_Form()
    if form.validate_on_submit():
        v_make = vehicle_make(
                make_type = form.make.data,
                capacity = form.capacity.data,
                cost_per_km = form.cost_per_km.data,
                no_of_loaders = form.no_of_loaders.data,
                driver_payment = form.driver_payment.data,
                loader_payment = form.loader_payment.data
                )
        try:
            db.session.add(v_make)
            db.session.commit()

            flask.flash('%r registered successfully'% form.make.data)
            return flask.redirect(flask.url_for('register.register_vehicle_make'))

        except IntegrityError:
            flask.flash('Vehicle type already exists. Please review your input.')

        except:
            flask.flash('An error occurred while saving the data. \
                    Please try again.')

    return flask.render_template('register/register_vehicle_make.html', form = form)


@register.route('/register_vehicle', methods = ['GET', 'POST'])
@flask_login.login_required
def register_vehicle():
    form = Vehicle_Form()

    makes = [(make.make_id, make.make_type) for make in 
            vehicle_make.query.order_by(vehicle_make.make_type.desc()).all()]

    form.make_id.choices = makes

    if form.validate_on_submit():
        v_vehicle = vehicle(
                plate_no = form.plate_no.data,
                make_id = form.make_id.data
                )
        try:
            db.session.add(v_vehicle)
            db.session.commit()

            flask.flash('%r registered successfully'% form.plate_no.data)
            return flask.redirect(flask.url_for('register.register_vehicle'))

        except IntegrityError:
            flask.flash('The vehicle is already registered. \
                    Please review your input.')

        except:
            flask.flash('An error occurred while saving the data. \
                    Please retry again.')

    return flask.render_template('register/register_vehicle.html', form = form)


@register.route('/member/register_small_scale_farmer/<int:member_id>', 
        methods = ['GET', 'POST'])
def register_small_scale_farmer(member_id):

    form = Small_Scale_Farmer_Form()

    if form.validate_on_submit():
        farmer = small_scale_farmer(
                first_name = form.first_name.data,
                middle_name = form.middle_name.data,
                last_name = form.last_name.data,
                gender = form.gender.data,
                date_of_birth = form.date_of_birth.data,
                email_address = form.email_address.data,
                phone_no = form.phone_no.data,
                residential_address = form.residential_address.data,
                group_id = member_id
                )
        try:
            db.session.add(farmer)
            db.session.commit()
            flask.flash("%r saved successfully"% form.first_name.data)
            return flask.redirect(
                    flask.url_for('register.register_small_scale_farmer', 
                        member_id = member_id)
                    )

        except IntegrityError:
            flask.flash('%r already exists. Please review your input.'\
                    % form.email_address.data)

        except:
            flask.flash('An error occurred while saving the data.')

    return flask.render_template('register/register_small_scale_farmer.html', 
            form = form)


@register.route('/register_driver', methods = ['GET', 'POST'])
@flask_login.login_required
def register_driver():

    form = Driver_Form()

    if form.validate_on_submit():
        d_driver = driver(
                first_name = form.first_name.data,
                middle_name = form.middle_name.data,
                last_name = form.last_name.data,
                gender = form.gender.data,
                date_of_birth = form.date_of_birth.data,
                email_address = form.email_address.data,
                phone_no = form.phone_no.data,
                residential_address = form.residential_address.data
                )
        try:
            db.session.add(d_driver)
            db.session.commit()
            flask.flash("Driver %r saved successfully"% form.first_name.data)
            return flask.redirect(
                    flask.url_for('register.register_driver')
                    )
        except IntegrityError:
            flask.flash('%r already exists. Please review your input.'\
                    % form.email_address.data)

        except:
            flask.flash("An error occurred while saving the record.")

    return flask.render_template('register/register_driver.html',
            form = form)


@register.route('/register_loader', methods = ['GET', 'POST'])
@flask_login.login_required
def register_loader():

    form = Loader_Form()

    if form.validate_on_submit():
        l_loader = loader(
                first_name = form.first_name.data,
                middle_name = form.middle_name.data,
                last_name = form.last_name.data,
                gender = form.gender.data,
                date_of_birth = form.date_of_birth.data,
                email_address = form.email_address.data,
                phone_no = form.phone_no.data,
                residential_address = form.residential_address.data
                )
        try:
            db.session.add(l_loader)
            db.session.commit()
            flask.flash("Loader %r saved successfully"% form.first_name.data)
            return flask.redirect(
                    flask.url_for('register.register_loader')
                    )
        except IntegrityError:
            flask.flash('%r already exists. Please review your input.'\
                    % form.email_address.data)

        except:
            flask.flash("An error occurred while saving the record.")

    return flask.render_template('register/register_loader.html',
            form = form)


@register.route('/register_offence', methods = ['GET', 'POST'])
@flask_login.login_required
def register_offence():                                                              
    form = Offence_Form()

    if form.validate_on_submit():
        o_offence = offence(
                description = form.description.data
                )
        try:
            db.session.add(o_offence)
            db.session.commit()
            flask.flash("Offence %r saved successfully"% form.description.data)
            return flask.redirect(
                    flask.url_for('register.register_offence')                                           )
        except IntegrityError:
            flask.flash('%r already exists. Please review your input.'\
                    % form.description.data)
        except:
            flask.flash("An error occurred while saving the record.")

    return flask.render_template('register/register_offence.html',
            form = form)


@register.route('/register_good', methods = ['GET', 'POST'])
@flask_login.login_required
def register_good():
    form = Good_Form()

    if form.validate_on_submit():
        g_good = good(
                description = form.description.data
                )
        try:
            db.session.add(g_good)
            db.session.commit()
            flask.flash("Item %r saved successfully"% form.description.data)
            return flask.redirect(
                    flask.url_for('register.register_good')
                    )
        except IntegrityError:
            flask.flash('%r already exists. Please review your input.'\
                    % form.description.data)
        except:
            flask.flash("An error occurred while saving the record.")
    return flask.render_template('register/register_good.html',
                    form = form)


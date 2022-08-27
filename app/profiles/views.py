import flask, flask_login, calendar
from sqlalchemy import func, and_
from datetime import datetime, date
from . import profiles
from .. import db
from .forms import Order_Form, Service_Form, Add_Order_Form
from ..decorators import permission_required, admin_required
from ..models import (member, small_scale_farmer, order, trip, vehicle, driver, 
        vehicle_make, service, Permission, role, user, loader, loader_assignment)


@profiles.route('/user/view_trips/<int:user_id>', methods = ['GET', 'POST'])
@flask_login.login_required
@permission_required(Permission.TRIPS)
def user_view_trips(user_id):
    response = flask.make_response(flask.redirect(
        flask.url_for('profiles.user_page', user_id = user_id)
        )
    )
    response.set_cookie('user_tab_var', '0', max_age = 60*60)
    return response


@profiles.route('/user/registrations/<int:user_id>', methods = ['GET', 'POST'])
@flask_login.login_required
@permission_required(Permission.REGISTRATION)
def user_registrations(user_id):
    response = flask.make_response(flask.redirect(
        flask.url_for('profiles.user_page', user_id = user_id)
        )
    )
    response.set_cookie('user_tab_var', '1', max_age = 60*60)
    return response


@profiles.route('/user/finance/<int:user_id>', methods = ['GET', 'POST'])
@flask_login.login_required
@permission_required(Permission.FINANCE)
def user_finance(user_id):
    response = flask.make_response(flask.redirect(
        flask.url_for('profiles.user_page', user_id = user_id)
        )
    )
    response.set_cookie('user_tab_var', '2', max_age = 60*60)

    return response


@profiles.route('/user/services/<int:user_id>', methods = ['GET', 'POST'])
@flask_login.login_required
@permission_required(Permission.SERVICES)
def user_services(user_id):
    response = flask.make_response(flask.redirect(
        flask.url_for('profiles.user_page', user_id = user_id)
        )
    )
    response.set_cookie('user_tab_var', '3', max_age = 60*60)
    return response


@profiles.route('/user/summary/<int:user_id>', methods = ['GET', 'POST'])
@flask_login.login_required
@permission_required(Permission.SUMMARY)
def user_summary(user_id):
    response = flask.make_response(flask.redirect(
        flask.url_for('profiles.user_page', user_id = user_id)
        )
    )
    response.set_cookie('user_tab_var', '4', max_age = 60*60)
    return response


@profiles.route('/user/graphs/<int:user_id>', methods = ['GET', 'POST'])
@flask_login.login_required
@permission_required(Permission.GRAPHS)
def user_graphs(user_id):
    response = flask.make_response(flask.redirect(
        flask.url_for('profiles.user_page', user_id = user_id)
        )
    )
    response.set_cookie('user_tab_var', '5', max_age = 60*60)

    return response


@profiles.route('/user/offenders/<int:user_id>', methods = ['GET', 'POST'])
@flask_login.login_required
@permission_required(Permission.OFFENDERS)
def user_offenders(user_id):
    response = flask.make_response(flask.redirect(
        flask.url_for('profiles.user_page', user_id = user_id)
        )
    )
    response.set_cookie('user_tab_var', '6', max_age = 60*60)

    return response


@profiles.route('/user_page/<int:user_id>',methods = ['GET', 'POST'])
@flask_login.login_required
def user_page(user_id):
    current_user = user.query.filter(user.id == user_id).first()
    user_role = role.query.filter(
            role.role_id == current_user.role_id).first()
    
    user_tab_variable = 5
    if flask.request.cookies.get('user_tab_var') is not None:
        user_tab_variable = int(flask.request.cookies.get('user_tab_var'))

    #view trips
    if user_tab_variable == 0:

        future_trips = trip.query.filter(trip.trip_date > datetime.utcnow())\
                .join(vehicle, vehicle.vehicle_id == trip.vehicle_id)\
                .join(driver, driver.driver_id == trip.driver_id)\
                .join(vehicle_make, vehicle_make.make_id == vehicle.make_id)\
                .add_columns(
                        trip.trip_id,
                        trip.trip_date,
                        vehicle.plate_no,
                        vehicle_make.make_type,
                        driver.driver_id,
                        driver.first_name,
                        driver.middle_name,
                        driver.last_name,
                        driver.phone_no,
                        trip.distance,
                        vehicle_make.cost_per_km,
                        vehicle_make.no_of_loaders,
                        vehicle_make.loader_payment,
                        vehicle_make.driver_payment
                        ).order_by(trip.trip_date.desc()).all()
        
        past_trips = trip.query.filter(trip.trip_date < datetime.utcnow())\
                .join(vehicle, vehicle.vehicle_id == trip.vehicle_id)\
                .join(driver, driver.driver_id == trip.driver_id)\
                .join(vehicle_make, vehicle_make.make_id == vehicle.make_id)\
                .add_columns(
                        trip.trip_id,
                        trip.trip_date,
                        vehicle.plate_no,
                        vehicle_make.make_type,
                        driver.driver_id,
                        driver.first_name,
                        driver.middle_name,
                        driver.last_name,
                        driver.phone_no,
                        trip.distance,
                        vehicle_make.cost_per_km,
                        vehicle_make.no_of_loaders,
                        vehicle_make.loader_payment,
                        vehicle_make.driver_payment
                        ).order_by(trip.trip_date.desc()).all()


        return flask.render_template('profiles/user_page.html',
                user_tab_variable = user_tab_variable, future_trips = future_trips, 
                past_trips = past_trips, user_role = user_role.name)

    #user registrations
    elif user_tab_variable == 1:
        return flask.render_template('profiles/user_page.html',
            user_tab_variable = user_tab_variable, user_role = role.name)

    elif user_tab_variable == 2:
        return flask.render_template('profiles/user_page.html',
            user_tab_variable = user_tab_variable, user_role = role.name)

    elif user_tab_variable == 3:

        form = Service_Form()

        vehicles = [((item.vehicle_id), (item.plate_no)) \
                for item in vehicle.query.order_by(vehicle.plate_no.desc()).all()]

        form.vehicle_id.choices = vehicles

        if flask.request.method == 'POST' and form.validate_on_submit():
            s_service = service(
                    vehicle_id = form.vehicle_id.data,
                    description = form.description.data,
                    cost = form.cost.data              
                    )
            try:
                db.session.add(s_service)
                db.session.commit()
                
                flask.flash('Service details saved successfully.')
                return flask.redirect(flask.url_for('profiles.user_services', 
                    user_id = user_id))
                
            except IntegrityError:
                db.session.rollback()
                flask.flash('An error occurred while saving the details of the \
                        service. Please try again.')

            except:
                flask.flash('An error occurred while saving the details of the \
                        service. Please try again.')


        services = service.query\
                .join(vehicle, vehicle.vehicle_id == service.vehicle_id)\
                .join(vehicle_make, vehicle_make.make_id == vehicle.make_id)\
                .add_columns(
                        service.service_id,
                        service.date,
                        service.cost,
                        service.description,
                        vehicle.plate_no,
                        vehicle_make.make_type
                        ).order_by(service.date.desc()).all()

        return flask.render_template('profiles/user_page.html',
            user_tab_variable = user_tab_variable, services = services, form = form,
            user_role = user_role.name)

    elif user_tab_variable == 4:
        #trip_count = db.session.query(func.count().label('no_of_trips'),
        #        #extract('year', trip.trip_date),
        #        #extract())
        monthly_data = {}

        months = {1 : 'January', 2 : 'February', 3 : 'March', 4 : 'April', 
                5 : 'May', 6 : 'June', 7 : 'July', 8 : 'August', 9 : 'September', 
                10 : 'October', 11 : 'November',12 : 'December'}

        today = datetime.now()
        year = today.strftime('%Y')
        month = today.strftime('%-m')
        number_of_days_in_current_month = calendar.monthrange(int(year), 
                int(month))[1]
        start_date = date(int(year), int(month), 1)
        end_date = date(int(year), int(month), number_of_days_in_current_month)

        daily_data = db.session.query(trip).filter(and_(
            trip.trip_date >= start_date, trip.trip_date <= end_date)).all()

        return flask.render_template('profiles/user_page.html',
            user_tab_variable = user_tab_variable, monthly_data = monthly_data, 
            daily_data = daily_data, user_role = user_role.name)

    elif user_tab_variable == 5:
        return flask.render_template('profiles/user_page.html', 
            user_tab_variable = user_tab_variable, user_role = user_role.name)

    elif user_tab_variable == 6:
        return flask.render_template('profiles/user_page.html',
            user_tab_variable = user_tab_variable, user_role = user_role.name)


    return flask.render_template('profiles/user_page.html',
            user_tab_variable = user_tab_variable, user_role = user_role.name)


@profiles.route('/member/make_order/<int:member_id>', methods = ['GET', 'POST'])
def make_order(member_id):
    response = flask.make_response(flask.redirect(
        flask.url_for('profiles.view_member_profile', member_id = member_id)
        )
    )
    response.set_cookie('tab_var', '0', max_age = 60*60)

    return response


@profiles.route('/member/view_orders/<int:member_id>', methods = ['GET', 'POST'])
def view_orders(member_id):
    response = flask.make_response(flask.redirect(
        flask.url_for('profiles.view_member_profile', member_id = member_id)
        )
    )
    response.set_cookie('tab_var', '1', max_age = 60*60)

    return response


@profiles.route('/member/view_member_profile/<int:member_id>', 
        methods = ['GET', 'POST'])
def view_member_profile(member_id):
    m_member = member.query.filter_by(member_id = member_id).first()

    farmers = None
    if m_member.status == "group":
        farmers = small_scale_farmer.query\
                .filter_by(group_id = member_id)\
                .order_by(small_scale_farmer.farmer_id.desc())\
                .all()

    tab_variable = 0
    if flask.request.cookies.get('tab_var') is not None:
        tab_variable = int(flask.request.cookies.get('tab_var'))

    if tab_variable == 0:
        form = Order_Form()

        if form.validate_on_submit():
            o_order = order(
                    member_id = m_member.member_id,
                    retail_name = form.retail_name.data,
                    retail_location = form.retail_location.data,
                    retail_email = form.retail_email_address.data,
                    retail_phone_no = form.retail_phone_no.data,
                    order_date = form.order_date.data
                    )

            try:
                db.session.add(o_order)
                db.session.commit()
                flask.flash('order submitted successfully.')

                return flask.redirect(
                        flask.url_for('profiles.make_order', member_id = member_id)
                        )
            except:
                flask.flash('An error occurred while making the order. \
                        Please try again.')
        return flask.render_template('profiles/view_member_profile.html', 
                member = m_member, farmers = farmers, form = form, tab_variable = tab_variable)

    elif tab_variable == 1:
        orders = order.query.filter_by(member_id = member_id)\
                .order_by(order.order_id.desc())\
                .all()

        return flask.render_template('profiles/view_member_profile.html',
                member = m_member, farmers = farmers, orders = orders, 
                tab_variable = tab_variable)


    elif tab_variable == 2:
        return flask.render_template('profiles/view_member_profile.html',
                member = m_member, farmers = farmers)


    elif tab_variable == 3:
        return flask.render_template('profiles/view_member_profile.html',
                member = m_member, farmers = farmers)


    elif tab_variable == 4:
        return flask.render_template('profiles/view_member_profile.html',
                member = m_member, farmers = farmers)


    return flask.render_template('profiles/view_member_profile.html', 
            member = m_member, farmers = farmers, tab_variable = tab_variable)


@profiles.route('/view_trip_details/<int:trip_id>', methods = ['GET', 'POST'])
def view_trip_details(trip_id):
    form = Add_Order_Form()

    free_orders = order.query.filter(
            and_(order.trip_id == None, order.order_date >= datetime.now()))\
                    .join(member, member.member_id == order.member_id)\
                    .add_columns(
                            order.order_id,
                            member.name
                            ).all()

    free_orders = [((item.order_id), ("ORDER ID : " + str(item.order_id)\
            + " MEMBER : " + str(item.name))) for item in free_orders]

    form.order_id.choices = free_orders

    if flask.request.method == 'POST':
        if form.validate_on_submit():
            o_order = order.query.filter_by(order_id = form.order_id.data).first()
            o_order.trip_id = trip_id
            try:
                db.session.commit()
                flask.flash('Order ID %r added successfully.'% form.order_id.data)
                return flask.redirect(
                    flask.url_for('profiles.view_trip_details', trip_id = trip_id))
            except:
                db.session.rollback()
                flask.flash('An error occurred while adding the order to current \
                        trip. Please try again.')

    t_trip = trip.query.filter_by(trip_id = trip_id)\
            .join(driver, driver.driver_id == trip.driver_id)\
            .join(vehicle, vehicle.vehicle_id == trip.vehicle_id)\
            .join(vehicle_make, vehicle_make.make_id == vehicle.make_id)\
            .add_columns(
                    trip.trip_id,
                    trip.trip_date,
                    trip.distance,
                    driver.driver_id,
                    driver.first_name,
                    driver.last_name,
                    driver.middle_name,
                    vehicle.plate_no,
                    vehicle_make.make_type
                    ).first()
    allocated_orders = order.query.filter_by(trip_id = trip_id)\
                .join(member, member.member_id == order.member_id)\
                .add_columns(
                        order.order_id,
                        order.order_date,
                        order.retail_name,
                        order.retail_location,
                        order.retail_email,
                        order.retail_phone_no,
                        member.name
                        ).all()

    return flask.render_template('profiles/view_trip_details.html', trip = t_trip, 
            form = form, allocated_orders = allocated_orders, 
            current_time = datetime.utcnow())


@profiles.route('/driver/driver_assigned_trips/<int:driver_id>',
        methods = ['GET', 'POST'])
def driver_assigned_trips(driver_id):
    response = flask.make_response(flask.redirect(                                          flask.url_for('profiles.view_driver_profile', driver_id = driver_id)
        )
    )
    response.set_cookie('tab_var', '0', max_age = 60*60)
    return response


@profiles.route('/driver/driver_offenses/<int:driver_id>',
        methods = ['GET', 'POST'])
def driver_offenses(driver_id):
    response = flask.make_response(flask.redirect(                                          flask.url_for('profiles.view_driver_profile', driver_id = driver_id)
        )
    )
    response.set_cookie('tab_var', '1', max_age = 60*60)
    return response


@profiles.route('/driver/driver_financial_records/<int:driver_id>', 
        methods = ['GET', 'POST'])
def driver_financial_records(driver_id):
    response = flask.make_response(flask.redirect(                                          flask.url_for('profiles.view_driver_profile', driver_id = driver_id)
        )
    )
    response.set_cookie('tab_var', '2', max_age = 60*60)
    return response

@profiles.route('/view_driver_profile/<int:driver_id>', methods = ['GET', 'POST'])
def view_driver_profile(driver_id):
    driver_tab_variable = 0
    d_driver = driver.query.filter_by(driver_id = driver_id).first()
    return flask.render_template('profiles/view_driver_profile.html', 
            driver = d_driver, driver_tab_variable = driver_tab_variable)


@profiles.route('/loader/loader_assigned_trips/<int:loader_id>',
        methods = ['GET', 'POST'])
def loader_assigned_trips(loader_id):
    response = flask.make_response(flask.redirect(                                          flask.url_for('profiles.view_loader_profile', loader_id = loader_id)
        )
    )
    response.set_cookie('tab_var', '0', max_age = 60*60)
    return response


@profiles.route('/loader/loader_financial_records/<int:loader_id>',
        methods = ['GET', 'POST'])
def loader_financial_records(loader_id):
    response = flask.make_response(flask.redirect(
        flask.url_for('profiles.view_loader_profile', loader_id = loader_id)
        )
    )
    response.set_cookie('tab_var', '2', max_age = 60*60)
    return response


@profiles.route('/view_loader_profile/<int:loader_id>', methods = ['GET', 'POST'])
def view_loader_profile(loader_id):
    loader_tab_variable = 0
    d_loader = loader.query.filter_by(loader_id = loader_id).first()

    if loader_tab_variable == 0:
        future_trips = trip.query\
                .join(driver, driver.driver_id == trip.driver_id)\
                .join(vehicle, vehicle.vehicle_id == trip.vehicle_id)\
                .join(vehicle_make, vehicle_make.make_id == vehicle.make_id)\
                .join(loader, loader.loader_id == loader_id)\
                .add_columns(
                        trip.trip_id,
                        trip.trip_date,
                        trip.distance,
                        driver.driver_id,
                        driver.first_name,
                        driver.last_name,
                        driver.middle_name,
                        driver.phone_no,
                        vehicle.plate_no,
                        vehicle_make.make_type,
                        ).order_by(trip.trip_date.desc()).all()

    return flask.render_template('profiles/view_loader_profile.html',
            loader = d_loader, loader_tab_variable = loader_tab_variable, 
            future_trips = future_trips)




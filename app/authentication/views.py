import flask
import flask_login
from . import authentication
from .. import db
from ..models import member, role, user
from .forms import (Member_Form, Login_Form, User_Registration_Form, 
        User_Login_Form)


@authentication.route('/register_user', methods = ['GET', 'POST'])
def register_user():
    form = User_Registration_Form()
    
    roles = [((item.role_id), (item.name)) for item in role.query.all()]
    form.role_id.choices = roles

    if form.validate_on_submit():
        u_user = user(
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                gender = form.gender.data,
                email_address = form.email_address.data,
                phone_no = form.phone_no.data,
                residential_address = form.residential_address.data,
                date_of_birth = form.date_of_birth.data,
                password = form.password.data,
                role_id = form.role_id.data
                )
        try:
            db.session.add(u_user)
            db.session.commit()

            flask.flash('You can now login.')
            return flask.redirect(flask.url_for('authentication.login_user'))

        except:
            flask.flash('An error occurred while registering you. \
                    Please try again.')

    return flask.render_template('authentication/register_user.html', form = form)


@authentication.route('/login_user', methods = ['GET', 'POST'])
def login_user():
    form = User_Login_Form()
    
    if form.validate_on_submit():
        u_user = user.query.filter_by(email_address = form.email_address.data)\
                .first()
        if u_user is not None and u_user.verify_password(form.password.data):
            flask_login.login_user(u_user, form.remember_me.data)
            next = flask.request.args.get('next')
            if next is None or not next.startswith('/'):
                next = flask.url_for('profiles.user_page', user_id = u_user.id)
            return flask.redirect(next)
        flask.flash('Invalid names or password.')
    return flask.render_template('authentication/login_user.html', form = form)


@authentication.route('/logout_user')
@flask_login.login_required
def logout_user():
    flask_login.logout_user()
    flask.flash("You've been logged out.")
    return flask.redirect(flask.url_for('main.homepage'))


@authentication.route('/register_member', methods = ['GET', 'POST'])
def register_member():
    form = Member_Form()
    if form.validate_on_submit():
        mem = member(
                name = form.name.data,
                email_address = form.email_address.data,
                phone_no = form.phone_no.data,
                status = form.status.data,
                nature_of_produce = form.nature_of_produce.data,
                location_address = form.location_address.data,
                password = form.password.data
                )
        try:
            db.session.add(mem)
            db.session.commit()
            flask.flash('You can now login.')
            return flask.redirect(flask.url_for('authentication.login_member'))

        except IntegrityError:
            flask.flash('User already exists. Try again later')

        except:
            flask.flash('An error occurred while saving the data.')

    return flask.render_template('authentication/register_member.html', form = form)


@authentication.route('/login_member', methods = ['GET', 'POST'])
def login_member():
    form = Login_Form()

    if form.validate_on_submit():
        user = member.query.filter_by(email_address = form.email_address.data)\
                .first()
        if user.password == form.password.data:
            flask.flash('Login successful.')
            return flask.redirect(flask.url_for('profiles.view_member_profile',
                member_id = user.member_id))

    return flask.render_template('authentication/login_member.html',form = form)

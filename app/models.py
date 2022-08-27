from . import db, login_manager
import flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))


offender = db.Table('offender',
        db.Column('offender_id', db.Integer, primary_key = True),
        db.Column('driver_id', db.Integer, db.ForeignKey('driver.driver_id')),
        db.Column('offence_id', db.Integer, db.ForeignKey('offence.offence_id')),
        db.Column('date_committed', db.DateTime, default = datetime.utcnow)
        )

good_assignment = db.Table('good_assignment',
        db.Column('good_assignment_id', db.Integer, primary_key = True),
        db.Column('order_id', db.ForeignKey('order.order_id')),
        db.Column('good_id', db.ForeignKey('good.good_id')),
        db.Column('quantity', db.Integer, nullable = False)
        )

loader_assignment = db.Table('loader_assignment', 
        db.Column('loader_assignment_id', db.Integer, primary_key = True),
        db.Column('trip_id', db.ForeignKey('trip.trip_id')),
        db.Column('loader_id', db.ForeignKey('loader.loader_id')),
        db.Column('date_assigned', db.DateTime, default = datetime.utcnow),
        db.Column('last_updated', db.DateTime, default = datetime.utcnow, 
            onupdate = datetime.utcnow)
        )


class Permission:
    FINANCE = 1
    SERVICES = 2
    REGISTRATION = 4
    SUMMARY = 8
    TRIPS = 16
    GRAPHS = 32
    ADMIN = 64
    OFFENDERS = 128

class role(db.Model):
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    default = db.Column(db.Boolean, default = False, index = True)
    permissions = db.Column(db.Integer)

    users = db.relationship('user',backref = 'role', lazy = 'dynamic')

    def __init__(self, **kwargs):
        super(role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0


    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm


    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm


    def reset_permissions(self):
        self.permissions = 0


    def has_permission(self, perm):
        return self.permissions & perm == perm


    def __repr__(self):
        return '{%r}:{%r}'% (self.role_id, self.name)

    @staticmethod
    def insert_roles():
        roles = {'user' : [Permission.GRAPHS],
                'clerk' : [
                    Permission.REGISTRATION,
                    Permission.TRIPS,
                    Permission.GRAPHS
                    ],
                'lead mechanic' : [
                    Permission.SERVICES, 
                    Permission.GRAPHS
                    ],
                'accounts manager' : [
                    Permission.GRAPHS,
                    Permission.SUMMARY,
                    Permission.FINANCE
                    ],
                'administrator' : [
                    Permission.TRIPS,
                    Permission.SERVICES,
                    Permission.FINANCE,
                    Permission.SUMMARY,
                    Permission.OFFENDERS,
                    Permission.GRAPHS,
                    Permission.REGISTRATION
                    ]
                }

        default_role = 'user'

        for r in roles:
            Role = role.query.filter_by(name = r).first()

            if Role is None:
                Role = role(name = r)

            Role.reset_permissions()

            for perm in roles[r]:
                Role.add_permission(perm)

            Role.default = (Role.name == default_role)

            db.session.add(Role)
        db.session.commit()

    users = db.relationship('user', backref = 'role', lazy = 'dynamic')


class user(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(64), nullable = False)
    last_name = db.Column(db.String(64), nullable = False)
    gender = db.Column(db.String(32), nullable = False)
    date_of_birth = db.Column(db.DateTime, default = datetime.utcnow)

    email_address = db.Column(db.String(128), unique = True)
    phone_no = db.Column(db.String(32), unique = True)
    residential_address = db.Column(db.String(128))
    
    password_hash = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))


    def __repr__(self):
        return '{%r} : {%r}'% (self.id, user.email_address)


    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, **kwargs):
        super(user, self).__init__(**kwargs)
        if self.role is None:
            if self.email_address == flask.current_app.config['FLASKY_ADMIN_EMAIL']:
                self.role = role.query.filter_by(name = 'administrator').first()

    def can(self, perm):
       return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
       return self.can(permission.ADMIN)

    @staticmethod
    def insert_roles():

        admin_role = role.query.filter_by(name = 'administrator').first()
        default_role = role.query.filter_by(default = True).first()

        for u in user.query.all():
            if u.email_address == flask.current_app.config['FLASKY_ADMIN_EMAIL']:
                u.role == admin_role

            else:
                u.role = default_role

        db.session.commit()


class anonymous_user(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = anonymous_user



class member(db.Model):
    __tablename__ = 'member'

    member_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable = False)
    status = db.Column(db.String(64), nullable = False)
    email_address = db.Column(db.String(128), nullable = False)
    phone_no = db.Column(db.String(32), nullable = False)
    nature_of_produce = db.Column(db.String(128), nullable = False)
    location_address = db.Column(db.String(128), nullable = False)
    password = db.Column(db.String(128), nullable = False)
    registration_date = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow, 
            onupdate = datetime.utcnow
            )

    #relationships
    farmers = db.relationship('small_scale_farmer', lazy = 'dynamic',
            backref = db.backref('member'))
    orders = db.relationship('order', lazy = 'dynamic',
            backref = db.backref('member'))

    def __repr__(self):
        return '<%r %r>'% (self.member_id, self.name)


class small_scale_farmer(db.Model):
    __tablename__ = 'small_scale_farmer'

    farmer_id = db.Column(db.Integer, primary_key = True, index = True)

    first_name = db.Column(db.String(64), nullable = False)
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    gender = db.Column(db.String(32))
    date_of_birth = db.Column(db.DateTime, nullable = False)
    
    email_address = db.Column(db.String(225), nullable = False)
    phone_no = db.Column(db.String(64), nullable = False)
    residential_address = db.Column(db.String(255), nullable = False)

    registration_date = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow, 
            onupdate = datetime.utcnow)

    #relationships
    group_id = db.Column(db.Integer, db.ForeignKey('member.member_id'))


    def __repr__(self):
        return '<%r : %r>'% (self.farmer_id, self.first_name)


class driver(db.Model):
    __tablename__ = 'driver'

    driver_id = db.Column(db.Integer, primary_key = True, index = True)

    first_name = db.Column(db.String(64), nullable = False)
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    gender = db.Column(db.String(32))
    date_of_birth = db.Column(db.DateTime, nullable = False)

    email_address = db.Column(db.String(225), nullable = False)
    phone_no = db.Column(db.String(64), nullable = False)
    residential_address = db.Column(db.String(255), nullable = False)

    registration_date = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    #relationships
    offences = db.relationship('offence', secondary = offender, lazy = 'dynamic',
            backref = db.backref('driver'))

    trips = db.relationship('trip', lazy = 'dynamic', 
            backref = db.backref('driver'))

    def __repr__(self):
        return '<%r : %r>'% (self.driver_id, self.first_name)



class loader(db.Model):
    __tablename__ = 'loader'

    loader_id = db.Column(db.Integer, primary_key = True, index = True)

    first_name = db.Column(db.String(64), nullable = False)
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    gender = db.Column(db.String(32))
    date_of_birth = db.Column(db.DateTime, nullable = False)

    email_address = db.Column(db.String(225), nullable = False)
    phone_no = db.Column(db.String(64), nullable = False)
    residential_address = db.Column(db.String(255), nullable = False)

    registration_date = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    #relationships
    trips_assigned = db.relationship('trip', secondary = loader_assignment, 
            backref = db.backref('loader')
            )

    def __repr__(self):
        return '<%r : %r>'% (self.loader_id, self.first_name)


class vehicle_make(db.Model):
    __tablename__ = 'vehicle_make'

    make_id = db.Column(db.Integer, primary_key = True)
    make_type = db.Column(db.String(225), unique = True, index = True)
    capacity = db.Column(db.Integer)
    cost_per_km = db.Column(db.Integer)
    no_of_loaders = db.Column(db.Integer)
    loader_payment = db.Column(db.Integer)
    driver_payment = db.Column(db.Integer)

    #relationships
    vehicles = db.relationship('vehicle', lazy = 'dynamic', 
            backref = db.backref('vehicle_make')
            )

    def __repr__(self):
        return "{%r} {%r}"% (self.make_id, self.make_type)


class good(db.Model):
    __tablename__ = 'good'

    good_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(128), nullable = False)

    def __repr__(self):
        return '<%r : %r>'% (self.good_id, self.description)



class offence(db.Model):
    __tablename__ = 'offence'

    offence_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(255), nullable = False)

    def __repr__(self):
        return '<%r : %r>'% (self.offence_id, self.description)


class vehicle(db.Model):
    __tablename__ = 'vehicle'

    vehicle_id = db.Column(db.Integer, primary_key = True)
    plate_no = db.Column(db.String(32), nullable = False, unique = True)
    registration_date = db.Column(db.DateTime, default = datetime.utcnow)

    #relationships
    make_id = db.Column(db.Integer, db.ForeignKey('vehicle_make.make_id'))
    services = db.relationship('service', lazy = 'dynamic', 
            backref = db.backref('vehicle.vehicle_id')
            )
    trips = db.relationship('trip', lazy = 'dynamic',
            backref = db.backref('vehicle'))

    def __repr__(self):
        return '<%r : %r>'% (self.vehicle_id, self.plate_no)


class service(db.Model):
    __tablename__ = 'service'

    service_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(128), nullable = False)
    cost = db.Column(db.Integer, default = 0)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    #relationships
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'))


    def __repr__(self):
        return '<%r : %r>'% (self.service_id, self.description)

class order(db.Model):
    __tablename__ = 'order'

    order_id = db.Column(db.Integer, primary_key = True)
    order_date = db.Column(db.DateTime, default = datetime.utcnow)

    retail_name = db.Column(db.String(128), nullable = False)
    retail_location = db.Column(db.String(64), nullable = False)
    retail_email = db.Column(db.String(128), nullable = False)
    retail_phone_no = db.Column(db.String(32), nullable = False)

    date = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow, 
            onupdate = datetime.utcnow)

    #relationships
    member_id = db.Column(db.Integer, db.ForeignKey('member.member_id'))
    goods = db.relationship('good', secondary = good_assignment, lazy = 'dynamic', 
            backref = db.backref('order'))
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.trip_id'))

    def __repr__(self):
        return '<%r : %r>'% (self.order_id, self.order_date)


class trip(db.Model):
    __tablename__ = 'trip'

    trip_id = db.Column(db.Integer, primary_key = True)
    trip_date = db.Column(db.DateTime, default = datetime.utcnow)
    distance = db.Column(db.Integer, nullable = False)

    last_updated = db.Column(db.DateTime, default = datetime.utcnow, 
            onupdate = datetime.utcnow)

    #relationships
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.driver_id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'))

    orders = db.relationship('order', lazy = 'dynamic', 
            backref = db.backref('trip')
            )

    def __repr__(self):
        return '<%r : %r>'% (self.trip_id, self.trip_date)

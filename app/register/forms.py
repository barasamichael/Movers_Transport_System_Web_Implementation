import flask_wtf
from wtforms import (StringField, IntegerField, SubmitField, SelectField, 
        TextAreaField)
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import DateField
from ..models import (vehicle_make, small_scale_farmer, loader, driver, good, 
        vehicle)


class Vehicle_Make_Form(flask_wtf.FlaskForm):
    make = StringField('vehicle make', validators = [DataRequired()])
    capacity = IntegerField('vehicle capacity', validators = [DataRequired()])
    no_of_loaders = IntegerField('number of loaders', validators = [DataRequired()])
    cost_per_km = IntegerField('cost per kilometer', validators = [DataRequired()])
    driver_payment = IntegerField('driver payment', validators = [DataRequired()])
    loader_payment = IntegerField('loader payment', validators = [DataRequired()])
    submit = SubmitField('save')

    def validate_make(self, field):
        if vehicle_make.query.filter_by(make_type = field.data).first():
            raise ValidationError('Vehicle make already registered!')

class Vehicle_Form(flask_wtf.FlaskForm):
    plate_no = StringField('registration number/plate number', 
            validators = [DataRequired()])
    make_id = SelectField('vehicle make', validators = [DataRequired()])

    submit = SubmitField('submit')

    def validate_plate_no(self, field):
        if vehicle.query.filter_by(plate_no = field.data).first():
            raise ValidationError('Vehicle is already registered.')


class Small_Scale_Farmer_Form(flask_wtf.FlaskForm):
    first_name = StringField('first name', validators = [DataRequired()])
    middle_name = StringField('middle name', validators = [DataRequired()])
    last_name = StringField('last name', validators = [DataRequired()])
    gender = SelectField('gender', choices = ['male', 'female'], 
            validators = [DataRequired()])
    date_of_birth = DateField('date of birth', format = "%Y-%m-%d", 
            validators = [DataRequired()]
            )
    
    email_address = StringField('email address', 
            validators = [DataRequired(), Email()]
            )
    phone_no = StringField('phone number', validators = [DataRequired()])
    residential_address = StringField('residential address', 
            validators = [DataRequired()]
            )

    submit = SubmitField('save')

    def validate_email_address(self, field):
        if small_scale_farmer.query.filter_by(email_address = field.data).first():
            raise ValidationError('Email address already in use.')


class Driver_Form(flask_wtf.FlaskForm):
    first_name = StringField('first name', validators = [DataRequired()])
    middle_name = StringField('middle name', validators = [DataRequired()])
    last_name = StringField('last name', validators = [DataRequired()])
    gender = SelectField('gender', choices = ['male', 'female'],
            validators = [DataRequired()])
    date_of_birth = DateField('date of birth', format = "%Y-%m-%d",
            validators = [DataRequired()]
            )

    email_address = StringField('email address',
            validators = [DataRequired(), Email()]
            )
    phone_no = StringField('phone number', validators = [DataRequired()])
    residential_address = StringField('residential address',
            validators = [DataRequired()]
            )

    submit = SubmitField('save')

    def validate_email_address(self, field):
        if driver.query.filter_by(email_address = field.data).first():
            raise ValidationError('Email address already in use.')


class Loader_Form(flask_wtf.FlaskForm):
    first_name = StringField('first name', validators = [DataRequired()])
    middle_name = StringField('middle name', validators = [DataRequired()])
    last_name = StringField('last name', validators = [DataRequired()])
    gender = SelectField('gender', choices = ['male', 'female'],
            validators = [DataRequired()])
    date_of_birth = DateField('date of birth', format = "%Y-%m-%d",
            validators = [DataRequired()]
            )

    email_address = StringField('email address',
            validators = [DataRequired(), Email()]
            )
    phone_no = StringField('phone number', validators = [DataRequired()])
    residential_address = StringField('residential address',
            validators = [DataRequired()]
            )

    submit = SubmitField('save')

    def validate_email_address(self, field):
        if loader.query.filter_by(email_address = field.data).first():
            raise ValidationError('Email address already in use.')


class Offence_Form(flask_wtf.FlaskForm):
    description = TextAreaField('offense description', 
            validators = [DataRequired()]
            )

    submit = SubmitField('save')


class Offender_Form(flask_wtf.FlaskForm):
    driver_id = SelectField('driver', validators = [DataRequired()])
    offence_id = SelectField('offense', validators = [DataRequired()])
    date_committed = DateField('date offense was committed', 
            validators = [DataRequired()])
    submit = SubmitField('submit')


class Good_Form(flask_wtf.FlaskForm):
    description = TextAreaField('commodity description',
            validators = [DataRequired()]
            )

    submit = SubmitField('save')

    def validate_description(self, field):
        if good.query.filter_by(description = field.data).first():
            raise ValidationError('The commodity is already recorded.')


class Order_Form(flask_wtf.FlaskForm):
    order_date = DateField('enter date you would wish to have your commodities \
            delivered', validators = [DataRequired()])
    retail_name = StringField('name of retail outlet to be delivered to', 
            validators = [DataRequired()])
    retail_location = StringField('retail outlet location address', 
            validators = [DataRequired()])
    retail_email = StringField("retail outlet's email address", 
            validators = [DataRequired(), Email()])
    retail_phone_no = StringField("retail outlet's phone number", 
            validators = [DataRequired()])
    submit = SubmitField('submit')

class Trip_Form(flask_wtf.FlaskForm):
    driver_id = SelectField('select driver', validators = [DataRequired()])
    vehicle_id = SelectField('select vehicle', validators = [DataRequired()])
    trip_date = DateField('date scheduled for the trip', 
            validators = [DataRequired()])
    distance = IntegerField('distance covered', validators = [DataRequired()])
    submit = SubmitField('submit')

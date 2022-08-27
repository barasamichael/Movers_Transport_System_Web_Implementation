import flask_wtf
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, 
        SelectField)
from wtforms.validators import Length, Email, DataRequired, EqualTo
from wtforms.fields.html5 import DateField
from wtforms import ValidationError

from ..models import member, user

class User_Registration_Form(flask_wtf.FlaskForm):
    first_name = StringField('first name', validators = [DataRequired(), 
        Length(1, 64)])
    last_name = StringField('last name', validators = [DataRequired(),
        Length(1, 64)])
    gender = SelectField('gender', validators = [DataRequired()], 
            choices = [('male', 'male'), ('female', 'female')])
    date_of_birth = DateField('date of birth', validators = [DataRequired()])
    email_address = StringField('email address', validators = [DataRequired(),
        Length(1, 64), Email()])
    phone_no = StringField('phone number', validators = [DataRequired(),
        Length(1, 16)])
    residential_address = StringField('residential address', validators =
            [DataRequired(), Length(1, 64)])
    role_id = SelectField('role', validators = [DataRequired(), Length(1, 32)])

    password = PasswordField('password', validators = [DataRequired(),
        EqualTo('password_2', message = 'passwords must match.')])
    password_2 = PasswordField('confirm password', validators = [DataRequired()])
    submit = SubmitField('submit')

    def validate_email_address(self, field):
        if user.query.filter_by(email_address = field.data).first():
            raise ValidationError('email already in use.')


class Member_Form(flask_wtf.FlaskForm):
    name = StringField('group/organization name', validators = [DataRequired(), 
        Length(1, 64)])
    email_address = StringField('email address', validators = [DataRequired(), 
        Length(1, 64), Email()])
    phone_no = StringField('phone number', validators = [DataRequired(),
        Length(1, 16)])
    status = SelectField('status (whether large scale farmer/group)', choices = 
            [('large scale farmer', 'large scale farmer'), ('group', 'group')],
            validators = [DataRequired()])
    nature_of_produce = StringField('nature of produce', 
            validators = [DataRequired(), Length(1, 64)])
    location_address = StringField('location address', validators = 
            [DataRequired(), Length(1, 64)])
    password = PasswordField('password', validators = [DataRequired(), 
        EqualTo('password_2', message = 'passwords must match.')])
    password_2 = PasswordField('confirm password', validators = [DataRequired()]) 

    submit = SubmitField('submit')

    def validate_email_address(self, field):
        if member.query.filter_by(email_address = field.data).first():
            raise ValidationError('email already in use.')

    def validate_name(self,field):
        if member.query.filter_by(name = field.data).first():
            raise ValidationError('username already in use.')

class Login_Form(flask_wtf.FlaskForm):
    username = StringField('username', validators = [DataRequired(), Length(1, 64)])
    email_address = StringField('email address', validators = [DataRequired(), 
        Email(), Length(1, 64)])
    password = PasswordField('password', validators = [DataRequired(), 
        Length(1, 64)])
    remember = BooleanField('remember me')

    submit = SubmitField('submit')


class User_Login_Form(flask_wtf.FlaskForm):
    first_name = StringField('first name', validators = [DataRequired(), 
        Length(1, 64)])
    last_name = StringField('last name', validators = [DataRequired(),                      Length(1, 64)])
    email_address = StringField('email address', validators = [DataRequired(),
        Email(), Length(1, 64)])
    password = PasswordField('password', validators = [DataRequired(),
        Length(1, 64)])
    remember_me = BooleanField('remember me')

    submit = SubmitField('submit')



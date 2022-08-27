import flask_wtf
from wtforms import (StringField, SubmitField, SelectField, IntegerField, 
        TextAreaField)
from wtforms.validators import Length, DataRequired, Email
from wtforms.fields.html5 import DateField

class Add_Order_Form(flask_wtf.FlaskForm):
    order_id = SelectField('select order', validators = [DataRequired()])
    submit = SubmitField('add order')


class Service_Form(flask_wtf.FlaskForm):
    vehicle_id = SelectField('select vehicle', validators = [DataRequired()])
    description = TextAreaField('service description',
            validators = [DataRequired()])
    cost = IntegerField('total cost', validators = [DataRequired()])
    submit = SubmitField('submit')


class Order_Form(flask_wtf.FlaskForm):
    order_date = DateField('order date', validators = [DataRequired()])

    retail_name = StringField('retailer outlet', 
            validators =[DataRequired(), Length(1, 64)])

    retail_location = StringField('retailer location address',
            validators =[DataRequired(), Length(1, 64)])

    retail_email_address = StringField("retailer's email address", 
            validators = [DataRequired(), Length(1, 128), Email()])

    retail_phone_no = StringField("retailer's phone number", 
            validators = [DataRequired(), Length(1, 16)])

    submit = SubmitField('submit')

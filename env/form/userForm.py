from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    validators,
    IntegerField,
    StringField,
    SubmitField,
    PasswordField,
    DateField,
    SelectField
)
from wtforms.validators import (
    DataRequired,
    InputRequired,
    optional,
    Email,
    EqualTo,
    URL
)

...

class UserRegisterForm(FlaskForm):
    
    """Sign up for a user account."""
    name = StringField(
        'name', 
        [DataRequired()]
    )
    email = StringField(
        'Email',
        [
            Email(message='Not a valid email address.'),
            optional()
        ]
    )
    mobileNumber = IntegerField(
        'Mobile Number',
        [InputRequired()]
    )
    password = PasswordField(
        'Password',
        [
            DataRequired(message="Please enter a password."),
        ]
    )
    state = StringField(
        'State',
        [
            DataRequired()
        ]
    )
    district = StringField(
        'District',
        [
            DataRequired()
        ]
    )
    municipality = StringField(
        'Municipality',
        [
            DataRequired()
        ]
    )
    wardNo = IntegerField(
        'Ward No'
    )
    address = StringField(
        'Address',
        [DataRequired()]
    )
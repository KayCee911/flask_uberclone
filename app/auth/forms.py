from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,  SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[
    DataRequired(),
    Length(min=7, max=20, message="Enter a valid phone number")
])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', 
        choices=[('rider', 'Rider'), ('driver', 'Driver')], 
        validators=[DataRequired()]
    )
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

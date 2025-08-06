from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class RideRequestForm(FlaskForm):
    pickup_location = StringField('Pickup Location', validators=[DataRequired()])
    dropoff_location = StringField('Dropoff Location', validators=[DataRequired()])
    submit = SubmitField('Request Ride')

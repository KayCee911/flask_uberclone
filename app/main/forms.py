from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length

class RideRequestForm(FlaskForm):
    pickup = StringField('Pickup', validators=[DataRequired(), Length(min=2, max=255)])
    pickup_lat = HiddenField()
    pickup_lng = HiddenField()
    dropoff = StringField('Dropoff', validators=[DataRequired(), Length(min=2, max=255)])
    dropoff_lat = HiddenField()
    dropoff_lng = HiddenField()
    submit = SubmitField('Request Ride')

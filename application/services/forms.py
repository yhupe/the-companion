from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    DateField

)
from wtforms.validators import DataRequired, Email


class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    whatsapp_number = StringField("WhatsApp Number", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


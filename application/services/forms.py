from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,

)
from wtforms.validators import DataRequired, Email


class UserForm(FlaskForm):
    user_name = StringField("Username", validators=[DataRequired()])
    whatsapp_number = StringField("WhatsApp Number", validators=[DataRequired()])
    submit = SubmitField("Submit")


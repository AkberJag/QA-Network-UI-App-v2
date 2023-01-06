""" IP Address Form """

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, Optional


class AddForm(FlaskForm):
    """add IP Address form"""

    pc_name = StringField("Enter PC name", validators=[InputRequired()])

    ip_address = StringField("Enter IP Address")
    network_template = SelectField("Selecet network template")

    submit = SubmitField("Add IP Address")


class DeleteForm(FlaskForm):
    """delete IP Address form"""

    id = IntegerField("Enter id of the IP address")
    submit = SubmitField("Delete IP Address")

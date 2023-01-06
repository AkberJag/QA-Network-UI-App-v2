""" Network Template Form """

from markupsafe import Markup
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional
from wtforms import StringField, SubmitField, FloatField


class AddForm(FlaskForm):
    """add IP Network Template"""

    network_template_name = StringField(
        "Name of network template", validators=[InputRequired()]
    )

    bandwidth_restriction_upload = FloatField(
        Markup("Enter Bandwidth restriction - <em>max upload</em>"),
        validators=[Optional()],
    )

    bandwidth_restriction_download = FloatField(
        Markup("Enter Bandwidth restriction - <em>max download</em>"),
        validators=[Optional()],
    )

    dns_latency = FloatField("DNS Latency (In seconds)", validators=[Optional()])

    general_latency = FloatField(
        "General Latency (In seconds)", validators=[Optional()]
    )

    packet_loss = FloatField("Packet Loss %", validators=[InputRequired()])

    cidr_ip = StringField("Enter the IP address", validators=[Optional()])
    cidr_suffix = StringField("Enter suffix", validators=[Optional()])

    submit = SubmitField("Add Network template")

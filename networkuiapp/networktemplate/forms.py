""" Network Template Form """

from markupsafe import Markup
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional
from networkuiapp.utils import validate_ip_address_string
from networkuiapp.networktemplate.models import NetworkTemplate
from wtforms import StringField, SubmitField, FloatField, IntegerField


# fmt: off
class AddForm(FlaskForm):
    """add IP Network Template"""

    # This is a hidden field to get the id when we are updating
    update_id = IntegerField()

    network_template_name = StringField("Name of network template", validators=[InputRequired()])
    
    bandwidth_restriction_upload = FloatField(Markup("Enter Bandwidth restriction - <em>max upload</em>"),validators=[Optional()])
    bandwidth_restriction_download = FloatField(Markup("Enter Bandwidth restriction - <em>max download</em>"),validators=[Optional()])
    
    dns_latency = FloatField("DNS Latency (In seconds)", validators=[Optional()])
    general_latency = FloatField("General Latency (In seconds)", validators=[Optional()])
    packet_loss = FloatField("Packet Loss %", validators=[InputRequired()])
    
    cidr_ip = StringField("Enter the IP address", validators=[Optional()])
    cidr_suffix = StringField("Enter suffix", validators=[Optional()])
    
    submit = SubmitField("Add Network template")


    def validate(self):
        """Validate the form."""
        initial_validation = super(AddForm, self).validate()
        if not initial_validation:
            return False

        network_template_to_update = NetworkTemplate.query.get(self.update_id.data) if NetworkTemplate.query.get(self.update_id.data) else None
        
        # Validate if template name is existing or not
        if network_template_to_update:
            if (NetworkTemplate.query.filter_by(network_template_name=self.network_template_name.data).first() != None and network_template_to_update.network_template_name != self.network_template_name.data):
                self.network_template_name.errors.append(f"Template name <b>'{self.network_template_name.data}'</b> is already in use")
                return False
        elif (NetworkTemplate.query.filter_by(network_template_name=self.network_template_name.data).first() != None):
            self.network_template_name.errors.append(f"Template name <b>'{self.network_template_name.data}'</b> is already in use")
            return False

        # Check if the cidr prefix text is valid ip or not
        if not validate_ip_address_string(self.cidr_ip.data) and self.cidr_ip.data is not '':
            self.cidr_ip.errors.append(f"<b>'{self.cidr_ip.data}'</b> is not a valid IP address.")
            return False

        # Check if Suffix is missing
        if self.cidr_ip.data and not self.cidr_suffix.data:
            self.cidr_suffix.errors.append(f"Add the suffix {self.cidr_ip.data}/<b>----</b>")
            return False
        
        # Check if Prefix IP is missing
        if not self.cidr_ip.data and self.cidr_suffix.data:
            self.cidr_ip.errors.append(f"Add the Prefix IP <b>__.__.__.__</b>/{self.cidr_suffix.data}")
            return False
        
        # Form validation is successful
        return True

""" IP Address Form """

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from networkuiapp.ipaddress.models import IPAddress
from networkuiapp.networktemplate.models import NetworkTemplate
from wtforms import IntegerField, StringField, SubmitField, SelectField
from networkuiapp.utils import validate_ip_address_string, check_ip_belongs_subnet


# fmt: off
class AddForm(FlaskForm):
    """add IP Address form"""

    # This is a hidden field to get the id when we are updating
    update_id = IntegerField()

    pc_name = StringField("Enter PC name", validators=[InputRequired()])

    ip_address = StringField("Enter IP Address", validators=[InputRequired()])
    network_template = SelectField("Selecet network template", validators=[InputRequired()])

    submit = SubmitField("Add IP Address")


    def validate(self):
        """Validate the form."""
        initial_validation = super(AddForm, self).validate()
        if not initial_validation:
            return False

        ip_address_to_update = IPAddress.query.get(self.update_id.data) if self.update_id.data and IPAddress.query.get(self.update_id.data) else None

        # Check if the PC name is alreay there on the DB or not
        if ip_address_to_update:
            if IPAddress.query.filter_by(pc_name=self.pc_name.data).first() != None and ip_address_to_update.pc_name != self.pc_name.data:
                self.pc_name.errors.append(f"The name <b>'{self.pc_name.data}'</b> is already been taken, Choose something else.")
                return False
        elif IPAddress.query.filter_by(pc_name=self.pc_name.data).first() != None:
            self.pc_name.errors.append(f"The name <b>'{self.pc_name.data}'</b> is already been taken, Choose something else.")
            return False


        # Check the enterd IP address is a valid one or not
        if not validate_ip_address_string(self.ip_address.data):
            self.ip_address.errors.append(f"<b>'{self.ip_address.data}'</b> is not a valid IP address.")
            return False
        
        # Check if the IP address added to any templates
        if ip_address_to_update:
            if IPAddress.query.filter_by(ip_address=self.ip_address.data).first() != None and ip_address_to_update.ip_address != self.ip_address.data:
                self.ip_address.errors.append(f"This IP address <b>{self.ip_address.data}</b> is already in use.")
                return False
        elif IPAddress.query.filter_by(ip_address=self.ip_address.data).first() != None:
            self.ip_address.errors.append(f"This IP address <b>{self.ip_address.data}</b> is already in use.")
            return False



        selected_network_profile = NetworkTemplate.query.get(self.network_template.data)
        # check if the IP address is belong to the subnet
        if not check_ip_belongs_subnet(self.ip_address.data, selected_network_profile.cidr_notation) and selected_network_profile.cidr_notation is not None:
            self.ip_address.errors.append(f"This IP address <b>{self.ip_address.data}</b> is not in the range of subnet <b><em>{selected_network_profile.cidr_notation}</em></b>.")
            return False
        
        # Form validation is successful
        return True


"""
    * This is how we do a fields specific validation, but to validate every columns at once we use the validate fn
    * But it is raising the validation error instead of appending the error to the errors list
    * I think the error is a field specific propery
    * So to show the error we use the self.{fieldname}.errors.append
    def validate_pc_name(self, pc_name) -> None:
        '''Check if the PC name is alreay there on the DB or not

        Args:
            pc_name: pc name entered by the user in the form

        Raises:
            ValidationError: Raise this error if the PC name submitted by the user is already taken

            ! New thing learned: the function name must the validate_'filed name' for this to work
        '''
        if IPAddress.query.filter_by(pc_name=pc_name.data).first() != None:
            raise ValidationError(f"The name <b>'{pc_name.data}'</b> is already been taken, Choose something else.")

    def validate_ip_address(self, ip_address):
        '''Check if the IP address string a valid IP address and is already been added to any templates'''
        if IPAddress.query.filter_by(ip_address=ip_address.data).first() != None:
            raise ValidationError(f"This IP address <b>{ip_address.data}</b> is already in use.")

        if not validate_ip_address_string(ip_address.data):
            raise ValidationError(f"<b>'{ip_address.data}'</b> is not a valid IP address.")
"""

class DeleteForm(FlaskForm):
    """delete IP Address form"""

    id = IntegerField("Enter id of the IP address")
    submit = SubmitField("Delete IP Address")

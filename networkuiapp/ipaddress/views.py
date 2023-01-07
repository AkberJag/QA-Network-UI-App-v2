""" IP address views."""

from flask import flash
from flask import url_for
from flask import redirect
from flask import Blueprint
from markupsafe import Markup
from networkuiapp import config
from flask import render_template
from networkuiapp.ipaddress.forms import AddForm
from networkuiapp.ipaddress.models import IPAddress
from networkuiapp.utils import make_dropdown, flash_errors
from networkuiapp.networktemplate.models import NetworkTemplate

blueprint = Blueprint("ipaddress", __name__, url_prefix="/ipaddress")


@blueprint.route("/add", methods=["GET", "POST"])
def add():
    """Add new ip address"""
    form = AddForm()

    # make the network profile dropdown
    form.network_template.choices = make_dropdown(NetworkTemplate, "template_name")

    # check if a SSH script is configuring the firewall
    if config.is_a_script_running:
        flash("a script is running please wait before adding a new PC", "danger")
        return redirect(url_for("networktemplates.add"))

    if form.validate_on_submit():
        IPAddress.create(
            ip_address=form.ip_address.data,
            pc_name=form.pc_name.data,
            network_template=form.network_template.data,
        )
        flash(Markup(f"IP address added successfully"), "success")
        # todo: redirect to home
    flash_errors(form)
    return render_template("ipaddress/add_ip_address.html", form=form)

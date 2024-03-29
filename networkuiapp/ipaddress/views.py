""" IP address views."""

from flask import flash
from flask import url_for
from flask import redirect
from flask import Blueprint
from flask import render_template

from markupsafe import Markup
from networkuiapp import config

from networkuiapp.database import update_pc_count

from networkuiapp.utils import flash_errors
from networkuiapp.utils import make_dropdown
from networkuiapp.utils import make_cidr_range

from networkuiapp.ipaddress.forms import AddForm
from networkuiapp.ipaddress.models import IPAddress
from networkuiapp.networktemplate.models import NetworkTemplate
from networkuiapp.firewall_helpers.firewall_utils import make_json_endpoint

blueprint = Blueprint("ipaddress", __name__, url_prefix="/ipaddress")


@blueprint.route("/add", methods=["GET", "POST"])
def add():
    """Add new ip address"""

    # check if a SSH script is configuring the firewall
    if config.is_a_script_running:
        flash("a script is running please wait before adding a new PC", "danger")
        return redirect(url_for("networktemplates.list"))

    form = AddForm()

    # make the network profile dropdown
    form.network_template.choices = make_dropdown(
        NetworkTemplate, "network_template_name"
    )

    # if the network handicap is empty, ask the user to add one first before adding an ip
    if NetworkTemplate.query.all() == []:
        flash("Add a Network Template first to add an ip address", "warning")
        return redirect(url_for("networktemplates.add"))

    if form.validate_on_submit():

        IPAddress.create(
            ip_address=form.ip_address.data,
            pc_name=form.pc_name.data,
            network_template=form.network_template.data,
        )

        # update the 'no_of_pcs' columns in the Network Templates Table
        update_pc_count(IPAddress, NetworkTemplate, form.network_template.data)

        make_json_endpoint(IPAddress, NetworkTemplate)

        flash(Markup(f"IP address added successfully"), "success")
        return redirect(url_for("public.index"))
    else:
        flash_errors(form)

    # make a dict with template name and cidr limit to show the cidr limit in html page
    # when a template is selected from drop down
    subnets = make_cidr_range(
        NetworkTemplate.query.with_entities(
            NetworkTemplate.network_template_name, NetworkTemplate.cidr_notation
        )
    )
    return render_template("ipaddress/add_ip_address.html", form=form, subnets=subnets)


@blueprint.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    """Delete an ip address entry"""

    # check if a SSH script is configuring the firewall
    if config.is_a_script_running:
        flash("a script is running please wait before deleting a new PC", "danger")
        return redirect(url_for("networktemplates.list"))

    ip_address_to_delete = IPAddress.query.get(id)
    if ip_address_to_delete:
        IPAddress.delete(ip_address_to_delete)

        # update the 'no_of_pcs' columns in the Network Templates Table
        update_pc_count(
            IPAddress, NetworkTemplate, ip_address_to_delete.network_template
        )

        make_json_endpoint(IPAddress, NetworkTemplate)

        flash(f"IP Address deleted", "success")
    return redirect(url_for("public.index"))


@blueprint.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    """Update an ip address"""
    form = AddForm()

    # check if a SSH script is configuring the firewall
    if config.is_a_script_running:
        flash("a script is running please wait before updating a new PC", "danger")
        return redirect(url_for("networktemplates.list"))

    # check if a SSH script is configuring the firewall if not make a config
    else:
        make_json_endpoint(IPAddress, NetworkTemplate)

    # make the network profile dropdown
    form.network_template.choices = make_dropdown(
        NetworkTemplate, "network_template_name"
    )

    # make a dict with template name and cidr limit to show the cidr limit in html page
    # when a template is selected from drop down
    subnets = make_cidr_range(
        NetworkTemplate.query.with_entities(
            NetworkTemplate.network_template_name, NetworkTemplate.cidr_notation
        )
    )

    ip_address_to_update = IPAddress.query.get_or_404(id)

    if form.validate_on_submit():
        old_template_id = ip_address_to_update.network_template

        ip_address_to_update.update(
            pc_name=form.pc_name.data,
            ip_address=form.ip_address.data,
            network_template=form.network_template.data,
        )

        # update the 'no_of_pcs' columns in the Network Templates Table
        update_pc_count(
            IPAddress,
            NetworkTemplate,
            form.network_template.data,
            old_template_id=old_template_id,
        )

        make_json_endpoint(IPAddress, NetworkTemplate)

        flash(Markup(f"IP address updated successfully"), "success")
        return redirect(url_for("public.index"))
    else:
        flash_errors(form)

    return render_template(
        "ipaddress/update_ip_address.html",
        form=form,
        subnets=subnets,
        ip_address_to_update=ip_address_to_update,
    )

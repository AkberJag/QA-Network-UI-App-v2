""" IP address views."""

from flask import flash
from flask import url_for
from flask import redirect
from flask import Blueprint
from flask import render_template

from markupsafe import Markup
from networkuiapp import config

from networkuiapp.utils import flash_errors
from networkuiapp.utils import make_dropdown
from networkuiapp.utils import make_cidr_range

from networkuiapp.ipaddress.forms import AddForm
from networkuiapp.ipaddress.models import IPAddress
from networkuiapp.networktemplate.models import NetworkTemplate
from networkuiapp.firewall_helpers.firewall_utils import add_ip_to_firewall

blueprint = Blueprint("ipaddress", __name__, url_prefix="/ipaddress")


@blueprint.route("/add", methods=["GET", "POST"])
def add():
    """Add new ip address"""
    form = AddForm()

    # make the network profile dropdown
    form.network_template.choices = make_dropdown(
        NetworkTemplate, "network_template_name"
    )

    # if the network handicap is empty, ask the user to add one first before adding an ip
    if NetworkTemplate.query.all() == []:
        flash("Add a Network Template first to add an ip address", "warning")
        return redirect(url_for("networktemplates.add"))

    # check if a SSH script is configuring the firewall
    if config.is_a_script_running:
        flash("a script is running please wait before adding a new PC", "danger")
        return redirect(url_for("networktemplates.list"))

    if form.validate_on_submit():
        add_ip_to_firewall(form.ip_address.data, form.network_template.data)
        IPAddress.create(
            ip_address=form.ip_address.data,
            pc_name=form.pc_name.data,
            network_template=form.network_template.data,
        )
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
    ip_address_to_delete = IPAddress.query.get(id)
    if ip_address_to_delete:
        IPAddress.delete(ip_address_to_delete)
        flash(f"IP Address deleted", "success")
        # TODO: Add a script call to remove this IP address from the restriction
    return redirect(url_for("networktemplates.list"))


@blueprint.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    """Update an ip address"""
    form = AddForm()

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

    # check if a SSH script is configuring the firewall
    if config.is_a_script_running:
        flash("a script is running please wait before adding a new PC", "danger")
        return redirect(url_for("networktemplates.list"))

    if form.validate_on_submit():
        ip_address_to_update.update(
            pc_name=form.pc_name.data,
            ip_address=form.ip_address.data,
            network_template=form.network_template.data,
        )
        flash(Markup(f"IP address updated successfully"), "success")
        # todo: redirect to home
        return redirect(url_for("networktemplates.list"))
    else:
        flash_errors(form)

    return render_template(
        "ipaddress/update_ip_address.html",
        form=form,
        subnets=subnets,
        ip_address_to_update=ip_address_to_update,
    )

""" IP address views."""

from flask import flash
from flask import url_for
from flask import redirect
from flask import Blueprint
from markupsafe import Markup
from networkuiapp import config
from flask import render_template
from networkuiapp.utils import flash_errors
from networkuiapp.ipaddress.models import IPAddress
from networkuiapp.networktemplate.forms import AddForm
from networkuiapp.networktemplate.models import NetworkTemplate
from networkuiapp.firewall_helpers.firewall_utils import make_json_endpoint

blueprint = Blueprint("networktemplates", __name__, url_prefix="/networktemplates")


@blueprint.route("/add", methods=["GET", "POST"])
def add():
    """Add a network template"""
    form = AddForm()

    # check if a SSH script is configuring the firewall
    if config.is_a_script_running:
        flash("a script is running please wait before adding a new template", "danger")
        return redirect(url_for("public.index"))

    # check if a SSH script is configuring the firewall if not make a config
    else:
        make_json_endpoint(IPAddress, NetworkTemplate)

    if form.validate_on_submit():
        cidr_notation = (
            f"{form.cidr_ip.data}/{int(form.cidr_suffix.data)}"
            if form.cidr_ip.data
            else None
        )
        NetworkTemplate.create(
            network_template_name=form.network_template_name.data,
            cidr_notation=cidr_notation,
            bandwidth_restriction_upload=form.bandwidth_restriction_upload.data,
            bandwidth_restriction_download=form.bandwidth_restriction_download.data,
            dns_latency=form.dns_latency.data,
            general_latency=form.general_latency.data,
            packet_loss=form.packet_loss.data,
        )
        flash(Markup(f"Network template added successfully"), "success")
        return redirect(url_for("networktemplates.list"))

    else:
        flash_errors(form)
    return render_template("networkprofile/add_network_template.html", form=form)


@blueprint.route("/list", methods=["GET"])
def list():
    """List all network templates"""
    network_templates = NetworkTemplate.query.all()
    return render_template(
        "networkprofile/list_network_template.html", network_templates=network_templates
    )


@blueprint.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    """Delete a network template"""

    # check if a SSH script is configuring the firewall
    if config.is_a_script_running:
        flash(
            "a script is running please wait before deleting a new template", "danger"
        )
        return redirect(url_for("public.index"))

    # check if a SSH script is configuring the firewall if not make a config
    else:
        make_json_endpoint(IPAddress, NetworkTemplate)

    network_template_to_delete = NetworkTemplate.query.get(id)
    if network_template_to_delete:
        NetworkTemplate.delete(network_template_to_delete)
        flash(f"Network Template deleted", "success")
    return redirect(url_for("networktemplates.list"))


@blueprint.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    """update a network template"""
    form = AddForm()

    # check if a SSH script is configuring the firewall
    if config.is_a_script_running:
        flash(
            "a script is running please wait before deleting a new template", "danger"
        )
        return redirect(url_for("public.index"))

    # check if a SSH script is configuring the firewall if not make a config
    else:
        make_json_endpoint(IPAddress, NetworkTemplate)

    network_template_to_update = NetworkTemplate.query.get_or_404(id)

    if form.validate_on_submit():
        cidr_notation = (
            f"{form.cidr_ip.data}/{form.cidr_suffix.data}"
            if form.cidr_ip.data
            else None
        )

        network_template_to_update.update(
            network_template_name=form.network_template_name.data,
            cidr_notation=cidr_notation,
            bandwidth_restriction_upload=form.bandwidth_restriction_upload.data,
            bandwidth_restriction_download=form.bandwidth_restriction_download.data,
            dns_latency=form.dns_latency.data,
            general_latency=form.general_latency.data,
            packet_loss=form.packet_loss.data,
        )
        return redirect(url_for("networktemplates.list"))

    else:
        flash_errors(form)

    return render_template(
        "networkprofile/update_network_template.html",
        form=form,
        network_template_to_update=network_template_to_update,
    )

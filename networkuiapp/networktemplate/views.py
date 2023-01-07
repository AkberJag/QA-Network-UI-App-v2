""" IP address views."""

from flask import flash
from flask import Blueprint
from markupsafe import Markup
from networkuiapp import config
from flask import render_template
from networkuiapp.utils import flash_errors
from networkuiapp.networktemplate.forms import AddForm
from networkuiapp.networktemplate.models import NetworkTemplate

blueprint = Blueprint("networktemplates", __name__, url_prefix="/networktemplates")


@blueprint.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()

    if form.validate_on_submit():
        NetworkTemplate.create(
            template_name=form.network_template_name.data,
            cidr_notation=f"{form.cidr_ip.data}/{form.cidr_suffix}",
            bandwidth_restriction_upload=form.bandwidth_restriction_upload.data,
            bandwidth_restriction_download=form.bandwidth_restriction_download.data,
            dns_latency=form.dns_latency.data,
            general_latency=form.general_latency.data,
            packet_loss=form.packet_loss.data,
        )
        flash(Markup(f"Network template added successfully"), "success")
        # todo: redirect to home
    else:
        flash_errors(form)
    return render_template("networkprofile/add_network_template.html", form=form)

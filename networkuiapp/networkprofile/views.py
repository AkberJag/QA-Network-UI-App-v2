""" IP address views."""

from flask import Blueprint
from flask import render_template
from networkuiapp.networkprofile.models import NetworkTemplate
from networkuiapp.networkprofile.forms import AddForm

blueprint = Blueprint("networktemplates", __name__, url_prefix="/networktemplates")


@blueprint.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()

    if form.validate_on_submit():
        new_network_template = NetworkTemplate.create(
            template_name=form.network_template_name.data,
            cidr_notation=f"{form.cidr_ip.data}/{form.cidr_suffix}",
            bandwidth_restriction_upload=form.bandwidth_restriction_upload.data,
            bandwidth_restriction_download=form.bandwidth_restriction_download.data,
            dns_latency=form.dns_latency.data,
            general_latency=form.general_latency.data,
            packet_loss=form.packet_loss.data,
        )
    return render_template("networkprofile/add_network_template.html", form=form)

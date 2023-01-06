""" IP address views."""

from flask import Blueprint
from flask import render_template
from networkuiapp.ipaddress.forms import AddForm
from networkuiapp.ipaddress.models import IPAddress
from networkuiapp.networkprofile.models import NetworkTemplate
from networkuiapp.utils import make_dropdown

blueprint = Blueprint("ipaddress", __name__, url_prefix="/ipaddress")


@blueprint.route("/add", methods=["GET", "POST"])
def add():
    """Add new ip address"""
    form = AddForm()
    form.network_template.choices = [
        (g.id, g.template_name) for g in NetworkTemplate.query.all()
    ]

    return render_template("ipaddress/add_ip_address.html", form=form)

    # return render_template("ipaddress/add_ip_address.html")

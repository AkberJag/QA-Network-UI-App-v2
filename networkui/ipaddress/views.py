""" IP address views."""

from flask import Blueprint
from flask import render_template, flash
from networkui.config import is_a_script_running

blueprint = Blueprint(
    "ipaddress",
    __name__,
    url_prefix="/ipaddress",
    template_folder="templates/ipaddress/",
)


@blueprint.route("/add", methods=["GET", "POST"])
def add():
    """Add new ip address"""

    flash("this is a test flash", "danger")
    return render_template("ipaddress/add_ip_address.html")

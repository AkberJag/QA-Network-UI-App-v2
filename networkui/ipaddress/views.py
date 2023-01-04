""" IP address views.
This also acts as the home page
"""

from flask import Blueprint
from flask import render_template

blueprint = Blueprint(
    "ipaddress", __name__, url_prefix="/", template_folder="templates/ipaddress/"
)


@blueprint.route("/add", methods=["GET", "POST"])
def add():
    return "hi"

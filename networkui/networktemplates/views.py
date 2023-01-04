""" IP address views."""

from flask import Blueprint
from flask import render_template

blueprint = Blueprint(
    "networktemplates",
    __name__,
    url_prefix="/networktemplates",
    template_folder="templates/networktemplates/",
)


@blueprint.route("/add", methods=["GET", "POST"])
def add():
    return "hi"

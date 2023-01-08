from flask import Blueprint
from flask import render_template
from networkuiapp.database import db
from networkuiapp.ipaddress.models import IPAddress
from networkuiapp.networktemplate.models import NetworkTemplate

blueprint = Blueprint("public", __name__, url_prefix="/")


@blueprint.route("/")
def index():
    network_templates = NetworkTemplate.query.all()

    templates = {}
    for template in network_templates:
        templates[template.id] = {
            "pc": (
                db.session.query(IPAddress, NetworkTemplate)
                .select_from(IPAddress)
                .join(NetworkTemplate)
                .filter(IPAddress.network_template == template.id)
                .all()
            ),
            "template": template,
        }

    return render_template("public/home.html", templates=templates)

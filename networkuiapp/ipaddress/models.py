""" IP Address Model 

A new thing learned: To make a migration, we need to make sure our model is imported by the app.
In most cases views.py should do that. if not then migrate wont detect models.

"""
from networkuiapp.database import PkModel, Column, db, ReferenceCol


class IPAddress(PkModel):
    """An IP address with PC name and the network template"""

    __tablename__ = "ipaddress"

    pc_name = Column(db.Text, unique=True)
    ip_address = Column(db.Text, unique=True)

    network_template = ReferenceCol("networktemplates")

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

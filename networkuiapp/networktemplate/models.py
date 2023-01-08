""" Network Template Model """

from networkuiapp.database import PkModel, Column, db, relationship


class NetworkTemplate(PkModel):
    """A network template where different parameters of a network is configured"""

    __tablename__ = "networktemplates"

    network_template_name = Column(db.Text, unique=True)  # Eg: good network

    cidr_notation = Column(db.Text)  # Eg: 192.168.1.1/23

    bandwidth_restriction_upload = Column(db.Float)
    bandwidth_restriction_download = Column(db.Float)

    dns_latency = Column(db.Float)
    general_latency = Column(db.Float)
    packet_loss = Column(db.Float)

    # this is to hold the total number of pcs configured for a template
    # ? Question: is this a better way or joining 2 tables and counting is better?
    no_of_pcs = Column(db.Integer, default=0)

    # https://docs.sqlalchemy.org/en/14/orm/cascades.html
    # cascade will auto delete the child when the parent is deleted
    ip_address_id = relationship(
        "IPAddress",
        backref="networktemplates",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

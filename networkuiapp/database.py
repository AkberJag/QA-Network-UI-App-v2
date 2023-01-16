"""
DB-related helper utilities. Taken from database.py
file at https://github.com/cookiecutter-flask/cookiecutter-flask
more reference at https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/customizing/#abstract-models-and-mixins
"""


from networkuiapp.extensions import db

# Alias common SQLAlchemy names
Column = db.Column
relationship = db.relationship


class CRUDMixin:
    """
    Mixin that adds convenience methods for
    CRUD (create, read, update, delete) operations.
    """

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it in the database.

        Returns:
            DB Class Object: returns the created record
        """
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record

        Args:
            commit (bool, optional): flag whether to commit. Defaults to True.

        Returns:
            Db Class object: returns the updated record if committed,
            None otherwise
        """
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if commit:
            self.save()
            return self
        return None

    def save(self, commit=True):
        """Save the record.

        Args:
            commit (bool, optional): flag whether to commit. Defaults to True.

        Returns:
            Db Class object: returns the record saved to db session
        """
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database.

        Args:
            commit (bool, optional): flag whether to commit. Defaults to True.

        Returns:
            Db Class object: returns the updated record if committed,
            None otherwise
        """
        db.session.delete(self)
        if commit:
            db.session.commit()
            return self
        return None


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


class PkModel(Model):
    """
    Base model class that includes CRUD convenience methods,
    plus adds a 'primary key' column named 'id'.
    """

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID.

        Args:
            record_id (int): ID of record to get

        Returns:
            DB Class object: object identified by record_id if any,
            None otherwise
        """
        if any(
            (
                isinstance(record_id, (str, bytes)) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.get(int(record_id))
        return None


def ReferenceCol(tablename, nullable=False, pk_name="id", **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = ReferenceCol('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey("{0}.{1}".format(tablename, pk_name)), nullable=nullable, **kwargs
    )


def update_pc_count(
    IPAddress, NetworkTemplate, NetworkTemplate_ID, old_template_id=None
) -> None:
    """Update the 'no_of_pcs' column on a network tempate table

    Args:
        IPAddress: The IPAddress model added or updated
        NetworkTemplate: The NetworkTemplate model selected while adding/updating a new pc
        NetworkTemplate_ID: Network template's PK
        old_template_id: to decrement one from the current template if update operation is performing
    """

    NetworkTemplate.query.get_or_404(NetworkTemplate_ID).update(
        no_of_pcs=len(
            db.session.query(IPAddress, NetworkTemplate)
            .select_from(IPAddress)
            .join(NetworkTemplate)
            .filter(IPAddress.network_template == NetworkTemplate_ID)
            .all()
        )
    )

    if old_template_id:
        NetworkTemplate.query.get_or_404(old_template_id).update(
            no_of_pcs=len(
                db.session.query(IPAddress, NetworkTemplate)
                .select_from(IPAddress)
                .join(NetworkTemplate)
                .filter(IPAddress.network_template == old_template_id)
                .all()
            )
        )

from zou.app.models.serializer import SerializerMixin
from zou.app.models.base import BaseMixin

from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData, Column, Integer

from sqlalchemy_utils import UUIDType
from sqlalchemy.dialects.postgresql import JSONB

from zou.app import db
from zou.app.models.serializer import SerializerMixin
from zou.app.models.base import BaseMixin


plugin_metadata = MetaData()
PluginBase = declarative_base(metadata=plugin_metadata)


class Ticket(PluginBase, BaseMixin, SerializerMixin):
    """ 
    Allow to open an issue on a given task.
    """

    __tablename__ = "tickets_tickets"

    title = db.Column(db.Text())
    text = db.Column(db.Text())

    task_id = db.Column(
        UUIDType(binary=False), db.ForeignKey("task.id"), index=True
    )
    person_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("person.id"),
        nullable=False,
        index=True,
    )
    assignee_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("person.id"),
        default=None,
        index=True,
    )

from sqlalchemy import MetaData
from sqlalchemy.util import FacadeDict
from sqlalchemy.orm import declarative_base

from sqlalchemy_utils import UUIDType, ChoiceType

from zou.app import db
from zou.app.models.serializer import SerializerMixin
from zou.app.models.base import BaseMixin
from zou.app.utils.plugins import create_plugin_metadata


plugin_metadata = create_plugin_metadata("tickets") # plugin id
PluginBase = declarative_base(metadata=plugin_metadata)


TICKET_STATUSES = [
    ("open", "Open"),
    ("on hold", "On Hold"),
    ("closed", "Closed"),
]


class Ticket(PluginBase, BaseMixin, SerializerMixin):
    """
    Allow to open an issue on a given task.
    """

    __tablename__ = "plugin_tickets_tickets"

    title = db.Column(db.Text())
    text = db.Column(db.Text())
    status = db.Column(
        ChoiceType(TICKET_STATUSES), default="open", nullable=False
    )
    task_id = db.Column(
        UUIDType(binary=False), db.ForeignKey("task.id"), index=True
    )
    project_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("project.id"),
        nullable=True,
        index=True,
    )
    episode_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("entity.id"),
        nullable=True,
        index=True,
    )
    person_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("person.id"),
        nullable=True,
        index=True,
    )
    assignee_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("person.id"),
        nullable=True,
        index=True,
    )

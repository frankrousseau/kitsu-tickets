from sqlalchemy_utils import UUIDType, ChoiceType

from zou.app import db
from zou.app.models.serializer import SerializerMixin
from zou.app.models.base import BaseMixin


TICKET_STATUSES = [
    ("open", "Open"),
    ("on hold", "On Hold"),
    ("closed", "Closed"),
]


class Ticket(db.Model, BaseMixin, SerializerMixin):
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

    def present(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "text": self.text,
            "status": str(self.status),
            "task_id": str(self.task_id) if self.task_id else None,
            "project_id": str(self.project_id) if self.project_id else None,
            "episode_id": str(self.episode_id) if self.episode_id else None,
            "person_id": str(self.person_id) if self.person_id else None,
            "assignee_id": (
                str(self.assignee_id) if self.assignee_id else None
            ),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

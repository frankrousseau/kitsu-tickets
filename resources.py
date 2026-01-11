from flask_restful import Resource
from flask_jwt_extended import jwt_required

from .models import Ticket

from zou.app.utils import fields
from zou.app.mixin import ArgsMixin
from zou.app.services.exception import NotFound

from zou.app.services.persons_service import get_current_user
from zou.app.services.exception import NotFound


class TicketsResource(Resource, ArgsMixin):

    @jwt_required()
    def get(self):
        tickets = Ticket.query().all()
        return fields.serialize_list(tickets)

    @jwt_required()
    def post(self):
        person_id = get_current_user()["id"]
        args = self.get_args([
            ("title", "", True),
            ("text", "", True),
            ("status", "open", True),
            ("task_id", None, True),
            ("assignee_id", None, True),
            ("project_id", None, True),
            ("episode_id", None, True),
        ])
        ticket = Ticket(
            title=args["title"],
            text=args["text"],
            status=args["status"],
            task_id=args["task_id"],
            person_id=person_id,
            assignee_id=args["assignee_id"],
            project_id=args["project_id"],
            episode_id=args["episode_id"],
        )
        ticket.save()
        return ticket.serialize(), 201

class TicketResource(Resource):

    @jwt_required()
    def get(self, id):
        ticket = Ticket.query().get(id)
        if not ticket:
            raise NotFoundException("Ticket not found")
        return ticket.serialize()

    @jwt_required()
    def delete(self, id):
        ticket = Ticket.query().get(id)
        if not ticket:
            raise NotFound("Ticket not found")
        ticket.delete()
        return "", 204

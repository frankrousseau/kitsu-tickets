from uuid import UUID
from typing import Optional, Literal

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from pydantic import BaseModel, ValidationError

from zou.app.mixin import ArgsMixin

from . import services


class TicketCreateSchema(BaseModel):
    title: str
    text: str
    status: Literal["open", "on hold", "closed"] = "open"
    task_id: Optional[UUID] = None
    assignee_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    episode_id: Optional[UUID] = None


class TicketUpdateSchema(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    status: Optional[Literal["open", "on hold", "closed"]] = None
    task_id: Optional[UUID] = None
    assignee_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    episode_id: Optional[UUID] = None


class TicketsResource(Resource, ArgsMixin):

    @jwt_required()
    def get(self):
        tickets = services.get_all_tickets()
        return [t.present() for t in tickets]

    @jwt_required()
    def post(self):
        try:
            data = TicketCreateSchema(**request.get_json())
        except ValidationError as e:
            return {"error": e.errors()}, 400
        ticket = services.create_ticket(data.model_dump(mode="json"))
        return ticket.present(), 201


class TicketResource(Resource, ArgsMixin):

    @jwt_required()
    def get(self, ticket_id):
        self.check_id_parameter(ticket_id)
        ticket = services.get_ticket(ticket_id)
        if not ticket:
            return {"error": "Ticket not found"}, 404
        return ticket.present()

    @jwt_required()
    def put(self, ticket_id):
        self.check_id_parameter(ticket_id)
        ticket = services.get_ticket(ticket_id)
        if not ticket:
            return {"error": "Ticket not found"}, 404
        try:
            data = TicketUpdateSchema(**request.get_json())
        except ValidationError as e:
            return {"error": e.errors()}, 400
        updated = data.model_dump(exclude_unset=True, mode="json")
        ticket = services.update_ticket(ticket, updated)
        return ticket.present()

    @jwt_required()
    def delete(self, ticket_id):
        self.check_id_parameter(ticket_id)
        ticket = services.get_ticket(ticket_id)
        if not ticket:
            return {"error": "Ticket not found"}, 404
        services.delete_ticket(ticket)
        return "", 204

from flask_restful import Resource

from .models import Ticket
from zou.app.utils import fields


class Tickets(Resource):

    def get(self):
        tickets = Ticket.query().all()
        return fields.serialize_list(tickets)

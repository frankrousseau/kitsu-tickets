from .models import Ticket

from zou.app.services.persons_service import get_current_user


def get_all_tickets():
    return Ticket.get_all()


def get_ticket(ticket_id):
    return Ticket.get(ticket_id)


def create_ticket(data):
    person_id = get_current_user()["id"]
    return Ticket.create(
        title=data["title"],
        text=data["text"],
        status=data.get("status", "open"),
        task_id=data["task_id"],
        person_id=person_id,
        assignee_id=data.get("assignee_id"),
        project_id=data.get("project_id"),
        episode_id=data.get("episode_id"),
    )


def update_ticket(ticket, data):
    ticket.update(data)
    return ticket


def delete_ticket(ticket):
    ticket.delete()

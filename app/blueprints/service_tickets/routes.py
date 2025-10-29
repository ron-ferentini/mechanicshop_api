from .schema import service_ticket_schema, service_tickets_schema, edit_service_ticket_schema
from app.models import Customer, Mechanic, Service_Ticket, db
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from . import service_tickets_bp
from ...utils.utils import customer_token_required

@service_tickets_bp.route('/service_tickets', methods=['POST'])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    query = select(Customer).where(Customer.id == service_ticket_data['customer_id'])
    customer = db.session.execute(query).scalars().first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    new_service_ticket = Service_Ticket(**service_ticket_data)
    db.session.add(new_service_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_service_ticket), 201

@service_tickets_bp.route('/service_tickets/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def update_service_ticket(ticket_id, mechanic_id):
    query = select(Service_Ticket).where(Service_Ticket.id == ticket_id)
    service_ticket = db.session.execute(query).scalars().first()
    if not service_ticket:
        return jsonify({"error": "Service Ticket not found"}), 404

    query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    
    service_ticket.mechanics.append(mechanic)
    db.session.commit()

    return jsonify({"message": "Mechanic assigned to Service Ticket"}), 200

@service_tickets_bp.route('/service_tickets/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['DELETE'])
def delete_service_ticket(ticket_id, mechanic_id):
    query = select(Service_Ticket).where(Service_Ticket.id == ticket_id)
    service_ticket = db.session.execute(query).scalars().first()
    if not service_ticket:
        return jsonify({"error": "Service Ticket not found"}), 404

    query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    if mechanic not in service_ticket.mechanics:
        return jsonify({"error": "Mechanic not assigned to this ticket"}), 400

    service_ticket.mechanics.remove(mechanic)
    db.session.commit()
    
    return jsonify({"message": "Service Ticket deleted"}), 200

@service_tickets_bp.route('/service_tickets', methods=['GET'])
def get_service_tickets():
    query = select(Service_Ticket)
    service_tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(service_tickets), 200

@service_tickets_bp.route('/service_tickets/<int:id>', methods=['GET'])
def get_service_ticket(id):
    query = select(Service_Ticket).where(Service_Ticket.id == id)
    service_ticket = db.session.execute(query).scalars().first()
    if service_ticket is None:
        return jsonify({"error": "Service Ticket not found"}), 404

    return service_ticket_schema.jsonify(service_ticket), 200

@service_tickets_bp.route('/my-tickets', methods=['GET'])
@customer_token_required
def get_my_service_tickets(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404
    
    query = select(Service_Ticket).where(Service_Ticket.customer_id == customer_id)
    service_tickets = db.session.execute(query).scalars().all()
    if not service_tickets:
        return jsonify({"error": "No service tickets found for this customer"}), 404
    
    return service_tickets_schema.jsonify(service_tickets), 200

@service_tickets_bp.route('/service_tickets/<int:ticket_id>', methods=['PUT'])
def edit_service_ticket(ticket_id):
    try:
        edit_service_ticket = edit_service_ticket_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    query = select(Service_Ticket).where(Service_Ticket.id == ticket_id)
    service_ticket = db.session.execute(query).scalars().first()
    if not service_ticket:
        return jsonify({"error": "Service Ticket not found"}), 404

    # Update the service ticket with the new data
    for mechanic_id in edit_service_ticket.get("add_mechanic_id", []):
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()
        if mechanic and mechanic not in service_ticket.mechanics:
            service_ticket.mechanics.append(mechanic)
            
    for mechanic_id in edit_service_ticket.get("remove_mechanic_id", []):
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()
        if mechanic and mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)

    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200
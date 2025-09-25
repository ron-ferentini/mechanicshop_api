from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from .schema import customer_schema, customers_schema
from .import customers_bp
from app.models import Service_Ticket, db, Customer

@customers_bp.route('/customers', methods=['POST'])
def create_customer():
   
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return {"errors": err.messages}, 400
    
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

@customers_bp.route('/customers', methods=['GET'])
def get_customers():
    
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(customers), 200

@customers_bp.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    query = select(Customer).where(Customer.id == id)
    customer = db.session.execute(query).scalars().first()
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404
    
    return customer_schema.jsonify(customer), 200

@customers_bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    query = select(Customer).where(Customer.id == id)
    customer = db.session.execute(query).scalars().first()
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404

    try:
        customer_data = customer_schema.load(request.json)
        
        customer.name = customer_data['name']
        customer.email = customer_data['email']
        customer.phone = customer_data['phone']
        
        db.session.commit() 
        return customer_schema.jsonify(customer), 200        
    except ValidationError as err:
        return {"errors": err.messages}, 400

@customers_bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    query = select(Customer).where(Customer.id == id)
    customer = db.session.execute(query).scalars().first()
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404

    query = select(Service_Ticket).where(Service_Ticket.customer_id == id)
    service_tickets = db.session.execute(query).scalars().all()
    if service_tickets:
        return jsonify({"error": "Cannot delete customer with existing service tickets"}), 400

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted"}), 200
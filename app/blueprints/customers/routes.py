from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from ...utils.utils import encode_token, token_required
from .schema import customer_schema, customers_schema, login_schema
from .import customers_bp
from app.models import Service_Ticket, db, Customer
from app.extensions import limiter, cache
from ...utils.utils import encode_token, token_required

#---------------------- Customer Login ----------------------#    
@customers_bp.route('/customers/login', methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as err:
        return jsonify(err.messages), 400

    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalars().first()
    if customer and customer.password == password:
        auth_token = encode_token(customer.id)

        response = {
            "status": "success",
            "message": "Successfully logged in.",
            "token": auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

#---------------------- Delete Customer by ID with Authentication and Constraint Check ----------------------#
@customers_bp.route('/customers', methods=['DELETE'])
@token_required
def delete_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404

    query = select(Service_Ticket).where(Service_Ticket.customer_id == customer_id)
    service_tickets = db.session.execute(query).scalars().all()
    if service_tickets:
        return jsonify({"error": "Cannot delete customer with existing service tickets"}), 400

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted"}), 200

#---------------------- Create Customer with Rate Limiting ----------------------#    
@customers_bp.route('/customers', methods=['POST'])
@limiter.limit("5/minute")
def create_customer():
   
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return {"errors": err.messages}, 400
    
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

#---------------------- Get All Customers with Caching ----------------------#
@customers_bp.route('/customers', methods=['GET'])
# @cache.cached(timeout=60, query_string=True)
def get_customers():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        query = select(Customer)
        customers = db.paginate(query, page=page, per_page=per_page, error_out=False)
        
        return customers_schema.jsonify(customers.items), 200
    except:  
        query = select(Customer)
        customers = db.session.execute(query).scalars().all()
        
        return  customers_schema.jsonify(customers), 200

#---------------------- Get Customer by ID with Authentication ----------------------#
@customers_bp.route('/customers', methods=['GET'])
@token_required
def get_customer(id):
    query = select(Customer).where(Customer.id == id)
    customer = db.session.execute(query).scalars().first()
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404
    
    return customer_schema.jsonify(customer), 200

#---------------------- Update Customer by ID with Authentication ----------------------#
@customers_bp.route('/customers/<int:id>', methods=['PUT'])
@token_required
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


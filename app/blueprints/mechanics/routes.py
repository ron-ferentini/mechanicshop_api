from app.utils.utils import encode_mechanic_token, mechanic_token_required
from .schema import mechanic_schema, mechanics_schema, login_schema
from app.models import Mechanic, Service_Ticket, db
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from . import mechanics_bp

#---------------------- Mechanic Login ----------------------#    
@mechanics_bp.route('/mechanics/login', methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as err:
        return jsonify(err.messages), 400

    query = select(Mechanic).where(Mechanic.email == email)
    mechanic = db.session.execute(query).scalars().first()
    if mechanic and mechanic.password == password:
        auth_token = encode_mechanic_token(mechanic.id)

        response = {
            "status": "success",
            "message": "Successfully logged in.",
            "token": auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401
    
@mechanics_bp.route('/mechanics', methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

@mechanics_bp.route('/mechanics', methods=['GET'])
def get_mechanics():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Mechanic)
        mechanics = db.paginate(query, page=page, per_page=per_page, error_out=False)
        
        return mechanics_schema.jsonify(mechanics.items), 200
    except:
        query = select(Mechanic).offset((page - 1) * per_page).limit(per_page)
        mechanics = db.session.execute(query).scalars().all()
        return mechanics_schema.jsonify(mechanics), 200

@mechanics_bp.route('/mechanics/<int:id>', methods=['GET'])
def get_mechanic(id):
    query = select(Mechanic).where(Mechanic.id == id)
    mechanic = db.session.execute(query).scalars().first()
    if mechanic is None:
        return jsonify({"error": "Mechanic not found"}), 404
    
    return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.route('/mechanics/<int:id>', methods=['PUT'])
def update_mechanic(id):
    query = select(Mechanic).where(Mechanic.id == id)
    mechanic = db.session.execute(query).scalars().first()
    if mechanic is None:
        return jsonify({"error": "Mechanic not found"}), 404

    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.route('/mechanics/popular', methods=['GET'])
def get_popular_mechanics():

    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()

    mechanics.sort(key=lambda mechanic: len(mechanic.service_tickets), reverse=True)

    return mechanics_schema.jsonify(mechanics), 200
 
@mechanics_bp.route('/mechanics/search', methods=['GET'])
def search_mechanics():
    name = request.args.get('name', '')
    email = request.args.get('email', '')
    phone = request.args.get('phone', '')

    query = select(Mechanic)

    if name:
        query = query.where(Mechanic.name.ilike(f'%{name}%'))
    if email:
        query = query.where(Mechanic.email.ilike(f'%{email}%'))
    if phone:
        query = query.where(Mechanic.phone.ilike(f'%{phone}%'))

    mechanics = db.session.execute(query).scalars().all()
    if mechanics is None or len(mechanics) == 0:
        return jsonify({"message": "No mechanics found matching the criteria"}), 404

    return mechanics_schema.jsonify(mechanics), 200
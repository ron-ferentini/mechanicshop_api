from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from .schema import inventory_schema, inventorys_schema
from .import inventory_bp
from app.models import Inventory, db
from app.extensions import cache

#---------------------- Inventory Routes ----------------------#
@inventory_bp.route('/inventory', methods=['POST'])
def create_inventory(): 
    try:
        inventory_data = request.get_json()
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_inventory = Inventory(**inventory_data)
    db.session.add(new_inventory)
    db.session.commit()
    
    return inventory_schema.jsonify(new_inventory), 201

#---------------------- Get All Inventory Items ----------------------#
@inventory_bp.route('/inventory', methods=['GET'])
def get_inventory_items():
    try:
        query = select(Inventory)
        inventory_items = db.session.execute(query).scalars().all()
        return inventorys_schema.jsonify(inventory_items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#---------------------- Get Single Inventory Item ----------------------#
@inventory_bp.route('/inventory/<int:inventory_id>', methods=['GET'])
def get_inventory_item(inventory_id):
    try:
        query = select(Inventory).where(Inventory.id == inventory_id)
        inventory_item = db.session.execute(query).scalars().first()
        if inventory_item is None:
            return jsonify({"error": "Inventory item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return inventory_schema.jsonify(inventory_item), 200

#---------------------- Delete Inventory Item ----------------------#
@inventory_bp.route('/inventory/<int:id>', methods=['DELETE'])
def delete_inventory_item(id):
    query = select(Inventory).where(Inventory.id == id)
    inventory_item = db.session.execute(query).scalars().first()
    if inventory_item is None:
        return jsonify({"error": "Inventory item not found"}), 404

    db.session.delete(inventory_item)
    db.session.commit()
    return jsonify({"message": "Inventory item deleted"}), 200  

#---------------------- Update Inventory Item ----------------------#
@inventory_bp.route('/inventory/<int:inventory_id>', methods=['PUT'])
def update_inventory_item(inventory_id):
    query = select(Inventory).where(Inventory.id == inventory_id)
    inventory_item = db.session.execute(query).scalars().first()
    if inventory_item is None:
        return jsonify({"error": "Inventory item not found"}), 404

    try:
        inventory_data = request.get_json()
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in inventory_data.items():
        setattr(inventory_item, key, value)

    db.session.commit()
    return inventory_schema.jsonify(inventory_item), 200
from flask import Blueprint, request, jsonify
from app import db
from app.models.yacht import Yacht

yacht_blueprint = Blueprint('yacht', __name__)

@yacht_blueprint.route('/yachts', methods=['GET'])
def get_yachts():
    yachts = Yacht.query.all()
    return jsonify([yacht.to_dict() for yacht in yachts])

@yacht_blueprint.route('/yachts', methods=['POST'])
def create_yacht():
    data = request.get_json()
    yacht = Yacht(**data)
    db.session.add(yacht)
    db.session.commit()
    return jsonify(yacht.to_dict()), 201

@yacht_blueprint.route('/yachts/<int:yacht_id>', methods=['GET'])
def get_yacht(yacht_id):
    yacht = Yacht.query.get(yacht_id)
    if yacht is None:
        return jsonify({'error': 'Yacht not found'}), 404
    return jsonify(yacht.to_dict())

@yacht_blueprint.route('/yachts/<int:yacht_id>', methods=['PUT'])
def update_yacht(yacht_id):
    yacht = Yacht.query.get(yacht_id)
    if yacht is None:
        return jsonify({'error': 'Yacht not found'}), 404
    data = request.get_json()
    yacht.name = data.get('name', yacht.name)
    yacht.description = data.get('description', yacht.description)
    yacht.capacity = data.get('capacity', yacht.capacity)
    yacht.price = data.get('price', yacht.price)
    db.session.commit()
    return jsonify(yacht.to_dict())

@yacht_blueprint.route('/yachts/<int:yacht_id>', methods=['DELETE'])
def delete_yacht(yacht_id):
    yacht = Yacht.query.get(yacht_id)
    if yacht is None:
        return jsonify({'error': 'Yacht not found'}), 404
    db.session.delete(yacht)
    db.session.commit()
    return jsonify({'message': 'Yacht deleted'})
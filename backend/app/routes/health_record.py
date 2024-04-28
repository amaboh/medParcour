
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, HealthRecord
from app.services.health_record_service import HealthRecordService

health_record_bp = Blueprint('health_record', __name__, url_prefix='/health-records')
health_record_service = HealthRecordService()

@health_record_bp.route('', methods=['POST'])
@jwt_required()
def create_health_record():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate and create the health record
    health_record = health_record_service.create_health_record(user_id, data)
    
    if health_record:
        return jsonify({'message': 'Health record created successfully', 'health_record': health_record}), 201
    else:
        return jsonify({'message': 'Failed to create health record'}), 400

@health_record_bp.route('', methods=['GET'])
@jwt_required()
def get_user_health_records():
    user_id = get_jwt_identity()
    
    # Retrieve the user's health records
    health_records = health_record_service.get_user_health_records(user_id)
    
    return jsonify({'health_records': health_records}), 200

@health_record_bp.route('/<int:health_record_id>', methods=['PUT'])
@jwt_required()
def update_health_record(health_record_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate and update the health record
    health_record = health_record_service.update_health_record(user_id, health_record_id, data)
    
    if health_record:
        return jsonify({'message': 'Health record updated successfully', 'health_record': health_record}), 200
    else:
        return jsonify({'message': 'Failed to update health record'}), 400
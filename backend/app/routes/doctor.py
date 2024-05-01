from flask import Blueprint, jsonify, request
from app.models import Doctor, HealthRecord, User, UserRecords, DoctorRemark
from app.services.doctor_service import DoctorService

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctors')
doctor_service = DoctorService()

@doctor_bp.route('/<int:doctor_id>/health-records', methods=['GET'])
def get_patient_health_records(doctor_id):
    health_records = doctor_service.get_patient_health_records(doctor_id)
    if health_records is None:
        return jsonify({'message': 'Doctor not found'}), 404

    return jsonify({'health_records': [record.serialize() for record in health_records]}), 200

@doctor_bp.route('/health-records/<int:health_record_id>/remarks', methods=['POST'])
def add_doctor_remark(health_record_id):
    data = request.get_json()
    doctor_id = data.get('doctor_id')
    remark = data.get('remark')

    result = doctor_service.add_doctor_remark(health_record_id, doctor_id, remark)
    if result == 'health_record_not_found':
        return jsonify({'message': 'Health record not found'}), 404
    elif result == 'doctor_not_found':
        return jsonify({'message': 'Doctor not found'}), 404
    elif result == 'missing_fields':
        return jsonify({'message': 'Missing required fields'}), 400

    return jsonify({'message': 'Remark added successfully'}), 201

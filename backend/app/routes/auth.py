# auth.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db, User, Doctor
from app.services.auth_services import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService()

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user_type = data.get('user_type')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')

    if not user_type or not name or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    if user_type == 'user':
        user = auth_service.register_user(name, email, password, phone)
    elif user_type == 'doctor':
        doctor = auth_service.register_doctor(name, email, password)
    else:
        return jsonify({'message': 'Invalid user type'}), 400

    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/settings', methods=['PUT'])
@jwt_required()
def settings():
    data = request.json
    user_id = get_jwt_identity()
    age = data.get('age')
    address = data.get('address')
    date_of_birth = data.get('date_of_birth')
    person_of_contact = data.get('person_of_contact')

    user_records = auth_service.register_user_records(user_id, age, address, date_of_birth, person_of_contact)
    return jsonify({'message': 'User records updated successfully'}), 200


@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')

    if not email or not password or not user_type:
        return jsonify({'message': 'Missing required fields'}), 400

    if user_type == 'user':
        user = auth_service.authenticate_user(email, password)
        if not user:
            return jsonify({'message': 'Invalid email or password'}), 401
        access_token = create_access_token(identity=user.id)
    elif user_type == 'doctor':
        doctor = auth_service.authenticate_doctor(email, password)
        if not doctor:
            return jsonify({'message': 'Invalid email or password'}), 401
        access_token = create_access_token(identity=doctor.id)
    else:
        return jsonify({'message': 'Invalid user type'}), 400

    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user:
        return jsonify(auth_service.get_user_details(user)), 200
    else:
        doctor = Doctor.query.get(user_id)
        if doctor:
            return jsonify(auth_service.get_doctor_details(doctor)), 200
        else:
            return jsonify({'message': 'User not found'}), 404
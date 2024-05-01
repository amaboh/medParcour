from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.conversation_service import ConversationService

conversation_bp = Blueprint('conversation', __name__, url_prefix='/conversations')
conversation_service = ConversationService()

@conversation_bp.route('/health-journal', methods=['GET'])
@jwt_required()
def get_health_journal():
    user_id = get_jwt_identity()
    conversation_history = conversation_service.get_user_conversation_history(user_id)
    return jsonify({'conversation_history': conversation_history}), 200

@conversation_bp.route('/initiate', methods=['POST'])
@jwt_required()
def initiate_conversation():
    user_id = get_jwt_identity()
    response = conversation_service.initiate_conversation(user_id)
    return jsonify({'response': response}), 200
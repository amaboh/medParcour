import os
from dotenv import load_dotenv
from app import db
from app.models import User, HealthRecord, Conversation
from app.services.health_record_service import HealthRecordService
from app.services.llm_service import LLMService
from app.utils.communication import get_user_phone_number
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

load_dotenv()

# Import or define the necessary Twilio credentials
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
TWILIO_NUMBER = 'your_twilio_number'

class ConversationService:
    def __init__(self):
        self.health_record_service = HealthRecordService()
        self.llm_service = LLMService()
        self.twilio_client = Client(account_sid, auth_token)
        self.twilio_number = TWILIO_NUMBER

    def get_user_conversation_history(self, user_id):
        conversations = Conversation.query.filter_by(user_id=user_id).order_by(Conversation.timestamp.desc()).all()
        return [conversation.serialize() for conversation in conversations]

    def create_conversation(self, user_id, content):
        conversation = Conversation(user_id=user_id, content=content)
        db.session.add(conversation)
        db.session.commit()
        return conversation.serialize()

    def initiate_conversation(self, user_id, phone_number):
        health_records = self.health_record_service.get_user_health_records(user_id)
        conversation_history = self.get_user_conversation_history(user_id)

        if health_records:
            latest_health_record = health_records[-1]
            medication_instructions = latest_health_record.medication_instructions
            prompt = f"Reminder: {medication_instructions}\n\nConversation History:\n{conversation_history}\n\nUser: Hello\nAssistant:"
        else:
            prompt = f"Conversation History:\n{conversation_history}\n\nUser: Hello\nAssistant:"

        response = self.llm_service.generate_response(prompt)
        self.create_conversation(user_id, f"Assistant: {response}")

        resp = VoiceResponse()
        resp.connect().stream(url="wss://c7e6-2a02-c7c-64a9-4200-78c9-b6d4-c93b-c7fe.ngrok-free.app/realtime")
        resp.say(response, voice='Polly.Amy')

        call = self.twilio_client.calls.create(
            twiml=str(resp),
            from_=self.twilio_number,
            to=phone_number,
        )
        print(f"Call initiated with SID: {call.sid}")

        return response
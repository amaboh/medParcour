from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client

class TwilioHandler:
    def __init__(self, account_sid, auth_token, twilio_number):
        self.client = Client(account_sid, auth_token)
        self.twilio_number = twilio_number

    def initiate_call(self, user_number):
        call = self.client.calls.create(
            to=user_number,
            from_=self.twilio_number,
            url="https://c7e6-2a02-c7c-64a9-4200-78c9-b6d4-c93b-c7fe.ngrok-free.app/answer"
        )
        return call.sid

    def build_response(self, say, gather=False):
        response = VoiceResponse()
        if gather:
            response.gather(input="speech", action="/process", method="POST")
        response.say(say)
        return str(response)

    def hangup_call(self):
        response = VoiceResponse()
        response.hangup()
        return str(response)
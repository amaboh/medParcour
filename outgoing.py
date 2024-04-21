import base64
import os
import json
import logging
import threading
import vertexai
from flask import Flask, render_template
from flask_sock import Sock
from twilio.rest import Client
from langchain_google_genai import ChatGoogleGenerativeAI
from transcription import SpeechClientBridge
from google.cloud.speech import RecognitionConfig, StreamingRecognitionConfig
from vertexai.language_models import ChatModel, InputOutputTextPair
from send_report import generate_report


app = Flask(__name__)
sockets = Sock(app)

HTTP_SERVER_PORT = 5000
TIWILIO_SAMPLE_RATE = 800  # Hz

# Twilio configuration
account_sid = os.environ('TWILIO_ACCOUNT_SID')
auth_token = os.environ('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)
TWILIO_NUMBER=os.environ('TWILIO_NUMBER')

# Google configuration
GOOGLE_PROJECT_ID = os.environ('GOOGLE_PROJECT_ID')
GOOGLE_API_KEY=os.environ('GOOGLE_API_KEY')
GOOGLE_LANGUAGE_CODE = 'en-US'


# Flask settings
PORT = 5000
DEBUG = False
INCOMING_CALL_ROUTE = '/'

# LangChain Google Generative AI setup
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

config = RecognitionConfig(
    encoding=RecognitionConfig.AudioEncoding.MULAW,
    sample_rate_hertz=8000,
    language_code="en-US",
)
streaming_config = StreamingRecognitionConfig(config=config, interim_results=True)
final_report=''

@app.route('/chat')
def streaming_prediction(
    project_id: str,
    location: str,
    res,
) -> str:
    
    """Streaming Chat Example with a Large Language Model"""

    vertexai.init(project=project_id, location=location)

    chat_model = ChatModel.from_pretrained("chat-bison")

    parameters = {
        "temperature": 0.8,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.95,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    chat = chat_model.start_chat(
        context="My name is Med_Ai. You are an health care assistant, knowledgeable about keeping track of health records.",
        examples=[
            InputOutputTextPair(
                input_text="I]m not feeling fine",
                output_text="Have you taken your drugs today",
            ),
        ],
    )

    responses = chat.send_message_streaming(
        message= f"{res}", **parameters)
    for response in responses:
        print(response.text)
        

@app.route("/twiml", methods=["POST"])
def return_twiml():
    print("POST TwiML")
    return render_template("streams.xml")


def on_transcription_response(response):
    transcription = ""  # Define response2 outside the loop
    global final_report

    if not response.results:
        return

    result = response.results[0]
    if not result.alternatives:
        return
    
    for result in response.results:
        if result.is_final:
            transcription = result.alternatives[0].transcript
            print("Transcription: " + transcription)
            final_report+=transcription
            final_report+=". "
            streaming_prediction(GOOGLE_PROJECT_ID, 'us-central1', transcription)


@sockets.route('/realtime')
def handle_media(ws):
    """Handles incoming media (audio) data from the Twilio call over a WebSocket connection."""
    app.logger.info("Connection accepted")
    bridge = SpeechClientBridge(streaming_config, on_transcription_response)
    t = threading.Thread(target=bridge.start)
    t.start()

    while True:
        message = ws.receive()
        if message is None:
            bridge.add_request(None)
            bridge.terminate()
            break

        data = json.loads(message)
        match data['event']:
            case "connected":
                print('twilio connected')
                continue
            case "start":
                print('twilio started')
                continue
            case "media": 
                payload_b64 = data['media']['payload']
                chunk = base64.b64decode(payload_b64)
                bridge.add_request(chunk)
            case "stop":
                print('twilio stopped')
                break

    bridge.terminate()
    print("WS connection closed")
    generate_report(final_report)


@app.route('/', methods=['GET', 'POST'])
def make_call(phone_number="+12403980310"):
    """Initiates an outbound call using Twilio."""
    # Generate the TwiML to connect the call to the WebSocket for media handling
    twiml = f"""
    <Response>
        <Connect>
            <Stream url="wss://13a2-2601-282-1d80-7b00-1561-4736-b44f-b6f0.ngrok-free.app/realtime" />
        </Connect>
        <Say>
            How are you feeling today?
        </Say>
    </Response>
    """.strip()

    # Make the outbound call
    call = client.calls.create(
        twiml=twiml,
        from_=TWILIO_NUMBER,
        to=phone_number,
    )
    
    return str(call.sid)

make_call("+12403980310")  # Uncomment this line to make the call when the application is run


if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    app.run(port=PORT, debug=DEBUG)

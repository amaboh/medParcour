import io
import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession
from dotenv import load_dotenv
from google.cloud import speech_v1p1beta1 as speech
import speech_recognition as sr
load_dotenv()
# Set up Google Cloud credentials

GOOGLE_PROJECT_ID = os.getenv('GOOGLE_PROJECT_ID')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/ama/Downloads/medparcour-16e08cede49a.json"

# Initialize Vertex AI
vertexai.init(project=GOOGLE_PROJECT_ID, location="us-central1")

# Load the Generative Language Model
model = GenerativeModel("gemini-1.0-pro")
chat = model.start_chat(response_validation=False)

import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession
import speech_recognition as sr

model = GenerativeModel("gemini-1.0-pro")
chat = model.start_chat(response_validation=False)

def get_chat_response(chat: ChatSession, prompt: str) -> str:
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)

def transcribe_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

while True:
    prompt = transcribe_speech()
    if prompt:
        response = get_chat_response(chat, prompt)
        print(f"Assistant: {response}")
import os
import base64
import base64
import google.auth
import datetime
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from langchain_google_genai import ChatGoogleGenerativeAI
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow



GOOGLE_API_KEY=os.environ('GOOGLE_API_KEY')

current_time = datetime.datetime.now()

SCOPES = ['https://mail.google.com/']

def gmail_send_message(result):
  """Create and send an email message
  Print the returned  message id
  Returns: Message object, including message id

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """  

  creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(
              'credentials.json', SCOPES)
          creds = flow.run_local_server(port=0)


  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    message.set_content(f"{result}")

    message["To"] = "amabocanon@gmail.com"
    message["From"] = "yorobrandon@gmail.com"
    message["Subject"] = f"Medical Report for Patient on {current_time}"

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

def generate_report(prompt):
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    result = llm.invoke(f"Write a detailed medical report to send to doctors based the following patient's information on {current_time} : {prompt}")
    print(result.content)
    gmail_send_message(result.content)

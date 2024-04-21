from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from langchain_google_genai import ChatGoogleGenerativeAI
from google.oauth2.credentials import Credentials
import os
import base64
import datetime
import json

# Get current date and time
current_datetime = datetime.datetime.now()

# Set up the credentials

creds = Credentials.from_authorized_user_info(info=json.load(f))

GOOGLE_API_KEY=os.environ['GOOGLE_API_KEY']

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

def generate_report(prompt):
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    result = llm.invoke(f"Write a detailed medical report for doctors based the following information : {prompt}")
    print(result.content)

# Create the Gmail API client
gmail = build('gmail', 'v1', credentials=creds)

# Define the email message
msg = MIMEText('This is the body of the email.')
msg['Subject'] = f'Medical report for patient1 on {current_datetime}'
msg['From'] = 'example@gmail.com'
msg['To'] = 'example@gmail.com'

# Send the email
try:
    message = (gmail.users().messages().send(userId='me', body={'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()})
                .execute())
    print(f'Message ID: {message["id"]}')
except Exception as e:
    print(f'An error occurred: {e}')
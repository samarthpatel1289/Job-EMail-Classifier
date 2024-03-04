from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import base64
import email
import datetime
import pickle
import os.path
import os


# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

EMAIL_LIST = []

def get_email_details(service, user_email, message_id):
    # Get a specific message with full format to get the headers
    msg = service.users().messages().get(userId=user_email, id=message_id, format='full').execute()

    # Fetch headers from the message and parse the required data
    headers = msg['payload']['headers']

    # Initialize variables for sender, subject, and body
    email_sender = None
    email_subject = None
    email_body = ""

    # Iterate through headers and find the sender and subject
    for header in headers:
        if header['name'] == 'From':
            email_sender = header['value']
        if header['name'] == 'Subject':
            email_subject = header['value']

    # Fetch the email body depending on its MIME type
    if 'parts' in msg['payload']:
        # This is a multipart message; walk through the payload parts to find the body
        for part in msg['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                email_body += base64.urlsafe_b64decode(part['body']['data'].encode('ASCII')).decode('utf-8')
                break  # We assume only one text/plain part
    else:
        # Non-multipart message; just decode the body
        email_body += base64.urlsafe_b64decode(msg['payload']['body']['data'].encode('ASCII')).decode('utf-8')

    return email_sender, email_subject, email_body


def get_gmail_service(email):
    pickle_token = f"tocken_{email}.pickle"
    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    if os.path.exists(pickle_token):
        with open(pickle_token, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(constants.EMAIL_CREDENTIAL_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(pickle_token, 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def check_emails(service, user_email):
    now = datetime.datetime.now()
    one_day_ago = now - datetime.timedelta(hours=24)
    query = f'after:{int(one_day_ago.timestamp())}'

    response = service.users().messages().list(userId=user_email, q=query).execute()

    messages = response.get('messages', [])

    email_list = []
    for message in messages:
        email_sender, email_subject, email_body = get_email_details(service, user_email, message['id'])
        email_list.append({
            "sender": email_sender,
            "subject": email_subject,
            "email": email_body
        })
    return email_list

    if not messages:
        print("No emails found.")
    else:
        print(f"Found {len(messages)} emails from the last hour:")
        for message in messages:
            # Fetch each full email's details
            email_sender, email_subject, email_body = get_email_details(service, message['id'])
            EMAIL_LIST.append({
                "sender" : email_sender,
                "subject" : email_subject,
                "email" :email_body
            })

if __name__ == '__main__':
    user_emails = ["samarthp1134@gmail.com", "patelsamarth787@gmail.com"]
    for user_email in user_emails:
        service = get_gmail_service(user_email)
        email_list = check_emails(service, user_email)
        print(f"Emails for: {user_email}")
        for email in email_list:
            print(email.get("sender"))
            print("-------------------")

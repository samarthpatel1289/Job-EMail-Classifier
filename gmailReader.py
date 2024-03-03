from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import base64
import email
import datetime
import pickle
import os.path

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

EMAIL_LIST = []

def get_gmail_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('samarth_email_cred.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run.
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_email_details(service, message_id):
    # Get a specific message with full format to get the headers
    msg = service.users().messages().get(userId='me', id=message_id, format='full').execute()

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


def check_emails(service):
    now = datetime.datetime.now()  # Get the current UTC time
    one_hour_ago = now - datetime.timedelta(hours=24)

    # Convert to UNIX timestamp (in seconds) and format the query string
    query = f'after:{int(one_hour_ago.timestamp())}'

    # Request a list of all messages in the Inbox that match the query
    response = service.users().messages().list(userId='me', q=query).execute()  # Removed labelIds parameter
    # response = service.users().messages().list(userId='me').execute()

    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])

    # Keep fetching messages if there are more than one page of results
    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
        messages.extend(response['messages'])

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
    service = get_gmail_service()
    label_response = service.users().labels().list(userId='me').execute()
    check_emails(service)
    for mails in EMAIL_LIST:
        print(mails.get("sender"))
        print("-------------------")

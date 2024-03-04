from dotenv import load_dotenv
load_dotenv()

from Gmail import gmailReader as read_emails
from Sheets import googleSheets as sheet
import LLM.job_email_classifier as classifier
import os
from bs4 import BeautifulSoup
from LLM import constants as const

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

    email_content = email.get("email")
    if bool(BeautifulSoup(email_content, "html.parser").find()):
        return extract_text_from_html(email_content)
    return html_content

def process_emails_and_update_sheet(email_address):
    # Read the emails from the given email address
    print(f"_________{email_address}_________")
    service = read_emails.get_gmail_service(email_address)
    email_list = read_emails.check_emails(service, email_address)

    # Iterate through each email and classify
    for email in email_list:

        response = classifier.classify_email(
            email.get("sender"),
            email.get("subject"),
            extract_text_from_html(email.get('email')),
        )
        classification, company, position = response.split(",")
        print(" - ",classification, ",", company, ",", position)

        # Check if the classification is 'job applied'
        if classification == const.JOB_APPLICATION_CONFIRMATION:
            # Write the details to the Google Sheet
            service = sheet.initialize_sheets_api(email_address)
            sheet.write_data_next_empty_row(service, os.getenv(f'SHEET_{email_address}'), "Sheet1", company, position, "")
        elif classification == const.JOB_REJECTION:
            service = sheet.initialize_sheets_api(email_address)
            sheet.find_and_update_status(service, os.getenv(f'SHEET_{email_address}'), "Sheet1!A1:E", company, position, "Rejection")

if __name__ == "__main__":
    emails_str = os.getenv('LIST_OF_EMAILS')
    if emails_str:
        list_of_emails = emails_str.split(',')
    else:
        list_of_emails = []

    for email in list_of_emails:
        process_emails_and_update_sheet(email)

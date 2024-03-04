import argparse
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
load_dotenv()

# Initialize the Sheets API client
def initialize_sheets_api(email):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    token_file = f"token_sheet_{email}.pickle"

    # Load previously saved credentials if they exist
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If credentials do not exist or are invalid, ask the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv("CREDENTIAL_PATH"), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service

def find_next_empty_row(service, spreadsheet_id, sheet_name):
    # Read the sheet data to find the first empty row
    range_name = f"{sheet_name}!A:A"  # Adjust if you need a different column to check
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    next_empty_row = len(values) + 1
    return next_empty_row

def write_data_next_empty_row(service, spreadsheet_id, sheet_name, company, position, resume):
    # Find the next empty row where we can write data
    next_empty_row = find_next_empty_row(service, spreadsheet_id, sheet_name)

    # Define the range to write data to
    range_name = f'{sheet_name}!A{next_empty_row}'

    data = [
        [company, position, "Applied", resume, "=TODAY()"]
    ]

    body = {
        'values': data
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='USER_ENTERED', insertDataOption='INSERT_ROWS', body=body).execute()
    print(f"        {result.get('updates').get('updatedCells')} cells updated.")

def find_and_update_status(service, spreadsheet_id, range_name, company, position, new_status):
    # Read the data from the sheet
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name).execute()
    values = result.get('values', [])

    # Find the headers for Company, Position and Status
    headers = values[0]  # Assuming the first row contains headers
    company_index = headers.index('Company')
    position_index = headers.index('Position')
    status_index = headers.index('Status')

    # Check against the hardcoded status 'Applied'
    desired_status = 'Applied'.lower()

    # Iterate over the rows to find the matching company, position, and status
    for idx, row in enumerate(values):
        if idx == 0:  # Skip header row
            continue
        if (len(row) > company_index and len(row) > position_index and len(row) > status_index):
            # Convert to lower case for case-insensitive comparison
            actual_company = row[company_index].lower()
            actual_position = row[position_index].lower()
            actual_status = row[status_index].lower()

            # Check if the current row matches the criteria
            if (actual_company == company.lower() and
                actual_position == position.lower() and
                actual_status == desired_status):

                # Match found, update the status in this row
                update_range = f"{range_name.split('!')[0]}!{chr(65 + status_index)}{idx + 1}"
                body = {
                    'values': [[new_status]]
                }

                service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id,
                    range=update_range,
                    valueInputOption='USER_ENTERED',
                    body=body).execute()

                print(f"        Status updated for {company}, {position} in cell {update_range}.")
                return

    # If no matching entry is found after searching all rows
    print(f"        No matching entry found for Company: '{company}', Position: '{position}' with Status 'Applied'.")

# Main function to parse arguments and call other functions
def main():
    parser = argparse.ArgumentParser(description="Update Google Sheets Data")
    subparsers = parser.add_subparsers(dest='action', help="Action to perform")

    # Global arguments
    parser.add_argument('--spreadsheet_id', required=True, help="The ID of the Google Spreadsheet")
    parser.add_argument('--sheet_name', default='Sheet1', help="Name of the worksheet")

    # Write action arguments
    parser_write = subparsers.add_parser('write', help="Write new data to the sheet")
    parser_write.add_argument('--company', required=True, help="Company name")
    parser_write.add_argument('--position', required=True, help="Position name")
    parser_write.add_argument('--resume', required=True, help="Resume link or text")

    # Update action arguments
    parser_update = subparsers.add_parser('update', help="Update existing data in the sheet")
    parser_update.add_argument('--range', required=False, help="Range to search within (for 'update' action)")
    parser_update.add_argument('--company', required=True, help="Company name to search (for 'update' action)")
    parser_update.add_argument('--position', required=True, help="Position name to search (for 'update' action)")
    parser_update.add_argument('--status', required=True, help="New status to write (for 'update' action)")

    args = parser.parse_args()

    # Initialize the Sheets API
    SERVICE_ACCOUNT_FILE = os.getenv("CREDENTIAL_PATH")
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = initialize_sheets_api("patelsamarth787@gmail.com")

    if args.action == 'write':
        write_data_next_empty_row(service, args.spreadsheet_id, args.sheet_name, args.company, args.position, args.resume)

    elif args.action == 'update':
        find_and_update_status(service, args.spreadsheet_id, "Sheet1!A1:E", args.company, args.position, args.status)

if __name__ == '__main__':
    main()

# python3 googleSheets.py write --company "Example Company" --position "Software Engineer" --resume "Infra"
# python3 googleSheets.py update --range 'Sheet1!A1:E' --company "Example Company" --position "Software Engineer" --status Offer
# '/Users/samarthpatel/Desktop/mailScripts/python/googleSheets.py'  update  --range ' Sheet1!A1:E ' --company ' Google LLC' --position ' unknown name' --status 'Rejection'

import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from soxm.Paths import Paths



# Path to the JSON service account key file
SERVICE_ACCOUNT_FILE = Paths.project('credentials.json') / 'credentials.json'

# Define the scope of the application
SCOPES = ["https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"]

# Use the service account credentials
creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Authenticate and create a gspread client
client = gspread.authorize(creds)

# Open the Google Sheet by name
spreadsheet_name = 'TestColabGoogleSheet'
spreadsheet = client.open(spreadsheet_name)

# Select the first worksheet
worksheet = spreadsheet.sheet1

def get_row_loc(worksheet):
    sheetvals = worksheet.get_all_values()
    rownum = len(sheetvals)
    return rownum

def write2sheets(row):
    # Data to write
    data = row
    
    # Clearing any existing content in the worksheet
    # worksheet.clear()

    # Find the first clear row to write new data
    rownum = get_row_loc(worksheet)

    # Writing data to the worksheet
    # The insert_rows method takes a list of lists as argument
    worksheet.insert_rows(data, rownum+1)
    
if __name__ == '__main__':
    data =  [
        ["NewHeader1", "Header2", "Header3"],
        ["Row1, Cell1", "Row1, Cell2", "Row1, Cell3"],
        ["Row2, Cell1", "Row2, Cell2", "Row2, Cell3"]
    ]
    write2sheets(data)
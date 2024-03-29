import datetime
import poplib
from email.parser import BytesParser
import csv
import time
import zipfile
import io

pop3_server = ''
username = ''
password = ''  # Be cautious with credentials
port = 995  # Common port for POP3 over SSL

local_npa_numbers = ['778', '250', '604']  # Example list
file_path = './output_file-%DATETIME%.csv'  # Replace with your actual file path

includeLocalCalls = True
includeOtherCalls = True
deleteMessages = False
periodicCheck = 60
timeCheck = 2

# Mode 1 = use mail server, 2 = use user input to process csv
mode = '2'


def process_account_code(code):
    """Process the account code to remove or add leading '1'."""
    if code.startswith('1') and len(code) == 9:
        return code[1:]  # Remove the leading '1' for 9-digit codes starting with '1'
    elif len(code) == 7:
        return '1' + code  # Prepend '1' to 7-digit codes
    elif len(code) == 8 and code.startswith('0'):
        return code
    return code


def is_local_call(to_number):
    """Determine if a call is local based on predefined NPA numbers."""
    npa = to_number.split(' ')[0][1:4]  # Extract NPA assuming format '(NPA) XXX-XXXX'

    return npa in local_npa_numbers


def process_csv_content(content):
    """Process and filter the CSV content based on account codes, call validity, and recent calls within the last 2
    minutes."""
    csv_reader = list(csv.reader(io.StringIO(content)))
    processed_calls = []
    last_account_code_by_extension = {}  # Track the last account code used by each extension
    csv_header = []

    name_index = None  # Variable to store the index of the "Name" field

    # Reverse the order of rows to process from oldest to newest
    for row in reversed(csv_reader):
        if row == "" or row == "\n":
            continue

        if row[0].__contains__("Type"):  # Skip header
            # Find and remove the "Name" field from the header
            # print(row.index("Name"))
            # name_index = row.index("Name")  # Adjust "Name" to the exact name of your field
            # del row[name_index]

            csv_header = row
            csv_header[0] = "Type"
            csv_header = csv_header + ["AccountCode"]
            continue

        if not row[1].__contains__("Outgoing"):
            continue

        # if name_index is not None:
        # Remove the "given name" field from each row based on its index
        # print("removing name index", name_index)
        # del row[name_index]

        call_type, direction, from_number, to_number, extension, *rest = row
        call_time = row[7] + " " + row[8]  # Assuming date is not used for comparison here

        # Define the format
        format_str = "%a %Y-%m-%d %I:%M %p"

        # Convert to datetime
        call_datetime = datetime.datetime.strptime(call_time, format_str)

        if len(to_number) <= 4:  # Skip extension to extension calls
            continue

        if len(to_number) in [7, 8, 9] and to_number.isdigit():
            account_code = process_account_code(to_number)
            # Update the last_account_code_by_extension with the timestamp
            last_account_code_by_extension[extension] = (account_code, call_datetime)
            continue

        # Check if the call was made within the last 2 minutes
        if extension in last_account_code_by_extension:
            last_account_code, last_code_time = last_account_code_by_extension[extension]
            if (call_datetime - last_code_time) <= datetime.timedelta(minutes=timeCheck):
                # Append account code to valid calls if within last 2 minutes
                processed_row = row + [last_account_code]
                processed_calls.append(processed_row)
                del last_account_code_by_extension[extension]

    new_list = list(reversed(processed_calls))

    # Reverse processed_calls to return to the original order with account codes appended
    return new_list, csv_header


def handle_zip_attachment(part):
    """Extract and process CSV files from a ZIP file attachment."""
    zip_file = io.BytesIO(part.get_payload(decode=True))
    with zipfile.ZipFile(zip_file) as z:
        for name in z.namelist():
            if name.endswith('.csv'):
                with z.open(name) as csv_file:
                    content = csv_file.read().decode('utf-8')
                    processed_calls, header = process_csv_content(content)

                    write_to_file(processed_calls, header)


def check_email_and_delete():
    """Check emails, process attachments, and mark messages for deletion."""
    mail = poplib.POP3_SSL(pop3_server, port)
    mail.user(username)
    mail.pass_(password)

    numMessages = len(mail.list()[1])
    for i in range(numMessages):
        raw_email = b"\n".join(mail.retr(i + 1)[1])
        parsed_email = BytesParser().parsebytes(raw_email)

        for part in parsed_email.walk():
            if part.get_content_maintype() == 'multipart':
                continue

            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if filename:
                if filename.endswith('.zip'):
                    handle_zip_attachment(part)
                elif filename.endswith('.csv'):
                    content = part.get_payload(decode=True).decode('utf-8')
                    processed_calls, header = process_csv_content(content)
                    write_to_file(processed_calls, header)
        if deleteMessages:
            print("Deleted message...")
            mail.dele(i + 1)  # Mark the message for deletion

    mail.quit()  # Ensure proper logout and deletion of marked messages


def write_to_file(processed_calls, header):
    processed_calls.insert(0, header)

    datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    file_name = file_path.replace("%DATETIME%", datetime_str)

    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(processed_calls)

    for call in processed_calls:
        print(call)


def main():
    if mode == '1':
        while True:
            print("Checking for new messages...")
            check_email_and_delete()
            print("Waiting for next check...")
            time.sleep(periodicCheck)
    elif mode == '2':
        csv_file_path = input("Enter the path to the CSV file: ")
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            content = csv_file.read()  # Read the content of the file into a string
            processed_calls, header = process_csv_content(content)  # Process the CSV content
            print(processed_calls)
            write_to_file(processed_calls, header)
    else:
        print("Invalid input. Exiting.")


if __name__ == '__main__':
    main()

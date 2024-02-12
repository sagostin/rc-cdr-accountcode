# RingCentral CDR Email Processing Script

This script automates the processing of Call Detail Records (CDR) logs emailed from RingCentral. It is designed to enhance billing procedures by appending account codes to calls, making the logs compatible with various billing software. The script filters and processes these logs, focusing on local calls and calls within a specified timeframe, and outputs a processed CSV file.

## Purpose

The main functionalities include:
- Filtering calls based on predefined NPA numbers to identify local calls.
- Processing valid calls within a specific timeframe for billing purposes.
- Appending account codes to filtered calls for integration with billing systems.
- Generating a processed CSV file for billing software.

## Dependencies

This script requires Python 3.x and the following libraries:
- `datetime`
- `poplib`
- `email.parser.BytesParser`
- `csv`
- `time`
- `zipfile`
- `io`

## Configuration

Before running the script, please configure the following parameters:

- `pop3_server`: Address of your mail server that receives RingCentral CDR emails.
- `username`: Username for accessing the mail server.
- `password`: Password for the mail server account. (Handle with care to ensure security)
- `port`: Typically set to 995 for POP3 over SSL.
- `local_npa_numbers`: List of NPA codes deemed as local for billing differentiation.
- `file_path`: The path and filename for the output CSV, incorporating `%DATETIME%` to include the current timestamp.
- Feature toggles: `includeLocalCalls`, `includeOtherCalls`, and `deleteMessages` flags can be adjusted based on your processing needs.
- `periodicCheck`: The interval in seconds for checking new emails.
- `timeCheck`: The timeframe in minutes to determine call validity for processing.

## Processing Logic

### Account Code Processing
Account codes are crucial for billing; the script processes incoming CDR logs to either append or modify account codes based on the call details.

### Local Call Determination
The script uses the `local_npa_numbers` configuration to identify local calls, aiding in billing categorization.

### CSV and ZIP Handling
Handles both direct CSV attachments and CSV files within ZIP attachments, ensuring all CDR logs are processed.

### Automated Email Handling
Automatically checks the configured mail server for new CDR logs, processes them according to the specified logic, and optionally deletes the emails post-processing.

## Execution

Run the script continuously on a server or a dedicated machine. It will periodically check for new emails, process the CDR logs as configured, and output a CSV file ready for billing software integration.

Ensure the mail server details are correctly configured and that the environment has the necessary Python dependencies installed before executing the script.

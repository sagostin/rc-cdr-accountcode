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

## Setting Up the Script as a Service

### On Windows

To run the script as a service in Windows, you can use `nssm` (the Non-Sucking Service Manager).

1. **Download NSSM**: First, download `nssm` from https://nssm.cc/download.
2. **Install the Service**: Open a command prompt as an administrator. Navigate to the directory where `nssm.exe` is located. Install the service using the following command, replacing `<path_to_python>` with the path to your Python executable (e.g., `C:\Python39\python.exe`), and `<path_to_script>` with the path to your script file:
`nssm install RingCentralCDRService "<path_to_python>" "<path_to_script>"`

3. **Configure the Service**: You can further configure the service (e.g., startup type, log on account) through the NSSM GUI that opens during installation or by using the `nssm edit RingCentralCDRService` command.

4. **Start the Service**: To start the service, use:
`nssm start RingCentralCDRService`


5. **Service Management**: You can stop or restart the service using `nssm stop RingCentralCDRService` or `nssm restart RingCentralCDRService`, respectively.

### On Linux

To set up the script as a service on a Linux system, you'll use `systemd`.

1. **Create a Service File**: Create a new service file in `/etc/systemd/system/` named `ringcentralcdr.service` with the following content, replacing `<path_to_python>` with the path to your Python executable and `<path_to_script>` with the full path to your script:

```
[Unit]
Description=RingCentral CDR Processing Service
After=network.target

[Service]
Type=simple
User=<username>
ExecStart=<path_to_python> <path_to_script>

[Install]
WantedBy=multi-user.target
```


1. **Reload Systemd**: Reload the systemd manager configuration to recognize the new service file:
`sudo systemctl daemon-reload`

2. **Enable the Service**: Enable the service to start on boot:
`sudo systemctl enable ringcentralcdr.service`

3. **Start the Service**: Start the service immediately:
`sudo systemctl start ringcentralcdr.service`

4. **Service Management**: You can manage the service (stop, start, restart) using systemd commands like `sudo systemctl stop ringcentralcdr.service`, `sudo systemctl start ringcentralcdr.service`, or `sudo systemctl restart ringcentralcdr.service`.




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


## Acknowledgments

This documentation and the accompanying script setup instructions were generated with assistance from ChatGPT, a language model developed by OpenAI. While most of the information provided has been verified for accuracy, there may be instances of discrepancies or areas for improvement. If you find any part of this documentation to be incorrect or if you have suggestions for enhancement, please feel free to open a pull request on the repository where this documentation is hosted. Your contributions are greatly appreciated in ensuring the accuracy and usefulness of this guide.

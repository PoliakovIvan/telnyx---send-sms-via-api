SMS Sending Script

This script reads phone numbers from a CSV file and sends SMS messages using the Telnyx API. If an SMS fails to send, it retries with an alternative sender number. If both attempts fail, the script logs the error and sends a notification to Slack.

Prerequisites

Python 3.x

Telnyx API key

Slack Webhook URL

Required Python packages (see Installation section)

Installation

Clone the repository or download the script.

Install required dependencies:

pip install python-dotenv telnyx requests

Create a .env file with the following environment variables:

TELNYX_API_KEY=your_telnyx_api_key
TELNYX_FROM_NUMBER=your_primary_sender_number
TELNYX_FROM_NUMBER_2=your_secondary_sender_number
TELNYX_MESSAGING_PROFILE_ID=your_telnyx_messaging_profile_id
SLACK_WEBHOOK_URL=your_slack_webhook_url

Usage

Prepare a CSV file (file_with_numbers.csv) containing phone numbers in the first column.

Each number must be formatted as 1XXXXXXXXXX (starting with 1 and followed by 10 digits).

If the phone numbers are in a different column, modify line[0] in the script to match the correct column index.

Run the script:

python script.py

Behavior

The script reads the CSV file line by line.

It sends an SMS to each number.

If sending fails, it retries with an alternative sender number.

If both attempts fail, the number is logged in error_log.csv, and a Slack notification is sent.

Successfully sent numbers are logged in success.csv.

The script waits 30 seconds between messages and pauses for a random time (100-200 seconds) every 200 messages to avoid rate limits.

Output Files

success.csv – logs successfully sent messages.

error_log.csv – logs failed messages.

Notes

Ensure your Telnyx account has an active messaging profile.

Check API rate limits to avoid restrictions.

Adjust the sleep time if necessary to comply with your SMS sending limits.

Troubleshooting

If numbers are not formatted correctly, check your CSV file.

If messages are not being sent, verify your Telnyx API key and messaging profile ID.

Check error_log.csv for numbers that failed to send.
import csv
import time
import random
import telnyx
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set Telnyx API key
telnyx.api_key = os.getenv("TELNYX_API_KEY")

def main():
    try:
        with open('file_with_numbers.csv', mode='r') as file:
            csv_reader = csv.reader(file)
            counter = 0
            
            for line in csv_reader:
                phone_number = line[0]  # Extract phone number from the line
                counter += 1
                
                if counter >= 200:
                    sleep_time = random.randint(100, 200)
                    print(f"Reached limit. Sleeping for {sleep_time} seconds...")
                    time.sleep(sleep_time)
                    counter = 0
                
                print(f"Processing number: {phone_number}")
                
                try:
                    time.sleep(30)
                    send_sms(phone_number, os.getenv("TELNYX_FROM_NUMBER"))
                    log_success(phone_number)
                except Exception as e:
                    print(f"Error sending to {phone_number}: {e}. Trying another number...")
                    try:
                        send_sms(phone_number, os.getenv("TELNYX_FROM_NUMBER_2"))
                        log_success(phone_number)
                    except Exception as e:
                        print(f"Final error: {phone_number} not sent. Logging error.")
                        slack_notification(phone_number)
                        log_error(phone_number)
    except FileNotFoundError:
        print("Error: file_with_numbers.csv not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")

def send_sms(to_num, from_num):
    # Send SMS via Telnyx API
    message = telnyx.Message.create(
        from_=from_num,
        messaging_profile_id=os.getenv("TELNYX_MESSAGING_PROFILE_ID"),
        to=f"+{to_num}",
        text="Your text",
        type="SMS"
    )
    print(f"SMS sent to {to_num} from {from_num}")

def slack_notification(error_num):
    # Send notification to Slack when SMS fails
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
    message = {"text": f"Can't send SMS to {error_num}"}
    response = requests.post(SLACK_WEBHOOK_URL, json=message)
    
    if response.status_code == 200:
        print("Slack notification sent successfully!")
    else:
        print(f"Failed to send Slack notification: {response.status_code}, {response.text}")

def log_success(phone_number):
    # Log successfully sent numbers
    with open('success.csv', mode='a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([phone_number])
    print(f"Logged success: {phone_number}")

def log_error(phone_number):
    # Log failed numbers
    with open('error_log.csv', mode='a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([phone_number])
    print(f"Logged error: {phone_number}")

if __name__ == "__main__":
    main()

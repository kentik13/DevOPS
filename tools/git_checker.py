import subprocess
import requests
from datetime import datetime

def get_git_diff(directory, user):
    try:
        # Run the git diff command and capture the output
        command = f"cd {directory} && sudo -u {user} git diff"
        result = subprocess.check_output(command, shell=True, universal_newlines=True)
        
        # Strip any leading or trailing whitespace from the result
        diff_output = result.strip()
        
        if diff_output:
            print("Git diff output detected.")
            return diff_output
        else:
            print("No changes detected in git diff.")
            return None
    
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running git diff: {e}")
        return None

def send_telegram_message(message, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # Define the maximum message length
    MAX_MESSAGE_LENGTH = 4096
    
    # Truncate the message if it exceeds the maximum length
    if len(message) > MAX_MESSAGE_LENGTH:
        message = message[:MAX_MESSAGE_LENGTH]
    
    data = {
        "chat_id": chat_id,
        "text": message
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        print(response.text)  # Print the response for debugging
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error sending message to Telegram: {e}")
        print(response.text)  # Print the response for debugging
        return False

def check_git_diff_and_notify(directory, user, bot_token, chat_id):
    diff_output = get_git_diff(directory, user)
    if diff_output:
        message = f"Git diff changes detected in {directory}:\n{diff_output}"
        if send_telegram_message(message, bot_token, chat_id):
            print(f"Git diff notification sent to Telegram.")
        else:
            print(f"Failed to send git diff notification to Telegram.")
    else:
        print(f"No changes detected in git diff for {directory}.")

# Example usage
if __name__ == "__main__":
    directory = "/var/www/"
    user = "user"
    bot_token = ""
    chat_id = ""

    if not bot_token or not chat_id:
        print("Please set the TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")
    else:
        check_git_diff_and_notify(directory, user, bot_token, chat_id)

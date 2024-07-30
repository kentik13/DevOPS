import ssl
import socket
from datetime import datetime
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings for unverified HTTPS requests
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

def get_ssl_expiry_date(hostname):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                not_after_str = cert.get('notAfter')
                if not_after_str:
                    expiry_date = datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z')
                    return expiry_date
                else:
                    print(f"Could not retrieve 'Not After' date from certificate for {hostname}.")
                    return None
    except ssl.SSLError as e:
        print(f"SSL error while retrieving certificate for {hostname}: {e}")
        return None
    except Exception as e:
        print(f"Error retrieving SSL certificate for {hostname}: {e}")
        return None

def send_telegram_message(message, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, data=data, timeout=10)  # Added timeout for better control
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error sending message to Telegram: {e}")
        return False

def check_ssl_expiry_and_notify(hostnames, bot_token, chat_id):
    for hostname in hostnames:
        expiry_date = get_ssl_expiry_date(hostname)
        if expiry_date:
            days_to_expiry = (expiry_date - datetime.utcnow()).days

            if days_to_expiry <= 5:
                message = f"Warning: SSL certificate for {hostname} is expiring in {days_to_expiry} days on {expiry_date}."
                if send_telegram_message(message, bot_token, chat_id):
                    print(message)
            else:
                print(f"SSL certificate for {hostname} is valid and will expire in {days_to_expiry} days on {expiry_date}.")
        else:
            print(f"Could not check SSL certificate for {hostname}.")

# Example usage
if __name__ == "__main__":
    hostnames = ["chat.bloomex.ca"]  # List of hostnames to check
    bot_token = ""
    chat_id = ""

    if not bot_token or not chat_id:
        print("Please set the TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")
    else:
        check_ssl_expiry_and_notify(hostnames, bot_token, chat_id)

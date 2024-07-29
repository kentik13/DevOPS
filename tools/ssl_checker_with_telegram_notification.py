import ssl
import socket
from datetime import datetime
import requests

def get_ssl_expiry_date(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            ssl_info = ssock.getpeercert()
            expiry_date_str = ssl_info['notAfter']
            expiry_date = datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y %Z')
            return expiry_date

def send_telegram_message(message, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=data)
    return response.status_code == 200

def check_ssl_expiry_and_notify(hostname, bot_token, chat_id):
    try:
        expiry_date = get_ssl_expiry_date(hostname)
        days_to_expiry = (expiry_date - datetime.utcnow()).days
        
        if days_to_expiry <= 5:
            message = f"SSL certificate for {hostname} is expiring in {days_to_expiry} days on {expiry_date}."
            if days_to_expiry < 0:
                message = f"SSL certificate for {hostname} has expired on {expiry_date}."
            send_telegram_message(message, bot_token, chat_id)
            print(message)
        else:
            print(f"SSL certificate for {hostname} is valid and will expire in {days_to_expiry} days on {expiry_date}.")
    except Exception as e:
        print(f"Could not check SSL certificate for {hostname}: {e}")
        send_telegram_message(f"Could not check SSL certificate for {hostname}: {e}", bot_token, chat_id)

# Example usage
websites = ["bloomex.ca", "bloomex.com.au", "bloomexusa.com"]
bot_token = "YOUR_TOKEN"
chat_id = "CHAT_IP"

# Print today's date at the beginning
current_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
print(f"Script run date and time: {current_date}")

for site in websites:
    check_ssl_expiry_and_notify(site, bot_token, chat_id)

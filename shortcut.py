import time
import threading
import pyperclip
from pynput import keyboard

PERSIAN_TO_ENGLISH = {
    'ض': 'q', 'ص': 'w', 'ث': 'e', 'ق': 'r', 'ف': 't',
    'غ': 'y', 'ع': 'u', 'ه': 'i', 'خ': 'o', 'ح': 'p',
    'ج': '[', 'چ': ']', 'ش': 'a', 'س': 's', 'ی': 'd',
    'ب': 'f', 'ل': 'g', 'ا': 'h', 'ت': 'j', 'ن': 'k',
    'م': 'l', 'ک': ';', 'گ': "'", 'ظ': 'z', 'ط': 'x',
    'ز': 'c', 'ر': 'v', 'ذ': 'b', 'د': 'n', 'پ': 'm',
    'و': ',', '؟': '?', ' ': ' ',
    '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5',
    '۶': '6', '۷': '7', '۸': '8', '۹': '9', '۰': '0',
}

typed_chars = []
typed_lock = threading.Lock()
modifier_keys = set()
MODIFIER_KEY_CODES = {
    keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r,
    keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
    keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r
}

def clear_old_keystrokes():
    while True:
        with typed_lock:
            now = time.time()
            typed_chars[:] = [(ch, t) for ch, t in typed_chars if now - t < 30]
        time.sleep(1)

def convert_persian_to_english(text):
    return ''.join(PERSIAN_TO_ENGLISH.get(ch, ch) for ch in text)

def capture_keystrokes():
    def on_press(key):
        try:
            # Track modifiers
            if key in MODIFIER_KEY_CODES:
                modifier_keys.add(key)
                return

            # Handle backspace
            if key == keyboard.Key.backspace:
                with typed_lock:
                    if typed_chars:
                        removed = typed_chars.pop()
                        # print(f"Backspac pressed: removed {removed[0]}")
                return

            # Detect Cmd + V → clear buffer
            if key == keyboard.KeyCode.from_char('v') and any(k in modifier_keys for k in {keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r}):
                with typed_lock:
                    typed_chars.clear()
                print("Paste. Buffer cleared.")
                return

            # Handle regular characters
            if key == keyboard.Key.space:
                char = ' '
            elif hasattr(key, 'char') and key.char:
                char = key.char
            else:
                return

            if modifier_keys:
                return  # Skip if any modifier is being held

            with typed_lock:
                typed_chars.append((char, time.time()))
            # print(f"[KEY] Recorded: {char}")
        except Exception as e:
            print(f"[ERROR] Keystroke: {e}")

    def on_release(key):
        modifier_keys.discard(key)

    keyboard.Listener(on_press=on_press, on_release=on_release).start()

def listen_hotkey():
    COMBO = {keyboard.Key.ctrl, keyboard.Key.shift, keyboard.KeyCode.from_char('p')}
    current_keys = set()

    def on_press(key):
        current_keys.add(key)
        if all(k in current_keys for k in COMBO):
            with typed_lock:
                recent_text = ''.join(ch for ch, _ in typed_chars)
                if recent_text and recent_text[-1] == 'p':
                    recent_text = recent_text[:-1]
            # print(f"[HOTKEY] Captured recent text: {recent_text}")
            if not recent_text:
                print("[HOTKEY] No recent text to convert.")
                return
            converted = convert_persian_to_english(recent_text)
            pyperclip.copy(converted)
            # print(f"[HOTKEY] Converted and copied: {converted}")

    def on_release(key):
        current_keys.discard(key)

    keyboard.Listener(on_press=on_press, on_release=on_release).start()

if __name__ == "__main__":
    print("🚀 Running... Type in Persian. Press Ctrl+Shift+P to convert.")
    threading.Thread(target=clear_old_keystrokes, daemon=True).start()
    capture_keystrokes()
    listen_hotkey()
    while True:
        time.sleep(1)

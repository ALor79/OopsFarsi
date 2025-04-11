# OopsFarsi

This script fixes accidentally typed Farsi text by converting it to the correct Latin characters based on physical Mac keyboard layout.

## 🚀 Features

- 🔡 Converts Persian characters (typed with Persian layout) to their equivalent English letters (as if typed with English layout).
- ⌨️ Listens for typing in the background and stores characters typed in the last 10 seconds.
- 🧠 Press `Ctrl + Shift + P` to convert and copy the last 10 seconds of typing to your clipboard.
- ❌ Ignores modifier-based shortcuts (`Cmd`, `Ctrl`, `Option`) like `Cmd+C`, `Cmd+V`.
- 🔙 Supports `Backspace` to remove from buffer.
- 📋 Automatically clears buffer when `Cmd+V` is pressed to avoid double typing.

## 🛠 Requirements

Install dependencies via pip by running:

```bash
pip install -r requirements.txt

# 🔐 Voice-Activated Password Locker

A Python app that manages your passwords using voice commands. Encrypts and stores passwords locally using the Fernet symmetric encryption.

## Features
- Speak to retrieve or add passwords
- Encrypts all data with Fernet
- Uses offline TTS (pyttsx3) and online STT (Google Speech API)

## Example Commands
- "Get password for Gmail"
- "Add password for GitHub"

## How to Run
```bash
pip install -r requirements.txt
python main.py

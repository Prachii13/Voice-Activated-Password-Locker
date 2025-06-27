import speech_recognition as sr
import pyttsx3
import json
import os
from cryptography.fernet import Fernet

DATA_FILE = "passwords.json"
KEY_FILE = "secret.key"

# Text-to-Speech
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Generate or load encryption key
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, 'wb') as f:
        f.write(Fernet.generate_key())

with open(KEY_FILE, 'rb') as f:
    key = f.read()

cipher = Fernet(key)

# Load password database
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print("🗣️ You said:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""

def get_password(site):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    if site in data:
        pwd = cipher.decrypt(data[site].encode()).decode()
        speak(f"The password for {site} is {pwd}")
    else:
        speak(f"No password found for {site}")

def add_password(site, password):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    data[site] = cipher.encrypt(password.encode()).decode()
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    speak(f"Password for {site} saved.")

def main():
    speak("Welcome to Voice Password Locker.")
    while True:
        command = listen()
        if 'get password for' in command:
            site = command.split('for')[-1].strip()
            get_password(site)
        elif 'add password for' in command:
            site = command.split('for')[-1].strip()
            speak(f"Say the password for {site}")
            pwd = listen()
            add_password(site, pwd)
        elif 'exit' in command:
            speak("Goodbye!")
            break
        else:
            speak("Try again with get or add password command.")

if __name__ == "__main__":
    main()

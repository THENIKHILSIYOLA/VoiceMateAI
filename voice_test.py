import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

engine.say("Hello Nikhil, VoiceMate AI is ready.")
engine.runAndWait()

with sr.Microphone() as source:
    print("🎤 Listening...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)

    print("You said:", text)

    engine.say("You said " + text)
    engine.runAndWait()

except sr.UnknownValueError:
    print("❌ I could not understand your voice.")

except sr.RequestError:
    print("❌ Speech recognition service is unavailable.")
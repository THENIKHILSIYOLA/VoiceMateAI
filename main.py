import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import datetime


# ==========================================
# VOICEMATE AI
# ==========================================

recognizer = sr.Recognizer()
engine = pyttsx3.init()

engine.setProperty("rate", 170)


# ==========================================
# SPEAK FUNCTION
# ==========================================

def speak(text):
    print("VoiceMate:", text)

    engine.say(text)
    engine.runAndWait()


# ==========================================
# LISTEN FUNCTION
# ==========================================

def listen():
    with sr.Microphone() as source:

        print("\n🎤 Listening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        except sr.WaitTimeoutError:
            print("❌ No voice detected.")
            return ""

    try:

        text = recognizer.recognize_google(audio)

        text = text.lower()

        print("You said:", text)

        return text

    except sr.UnknownValueError:

        print("❌ Sorry, I could not understand.")

        return ""

    except sr.RequestError:

        print("❌ Speech recognition service error.")

        return ""


# ==========================================
# COMMAND PROCESSOR
# ==========================================

def process_command(command):

    if command == "":
        return True


    # --------------------------------------
    # GREETING
    # --------------------------------------

    if "hello" in command or "hi" in command:

        speak("Hello Nikhil! How can I help you?")


    # --------------------------------------
    # NAME
    # --------------------------------------

    elif "what is my name" in command:

        speak("Your name is Nikhil.")


    # --------------------------------------
    # TIME
    # --------------------------------------

    elif "time" in command:

        current_time = datetime.now().strftime("%I:%M %p")

        speak("The current time is " + current_time)


    # --------------------------------------
    # DATE
    # --------------------------------------

    elif "date" in command:

        current_date = datetime.now().strftime(
            "%d %B %Y"
        )

        speak("Today's date is " + current_date)


    # --------------------------------------
    # YOUTUBE
    # --------------------------------------

    elif "open youtube" in command:

        speak("Opening YouTube.")

        webbrowser.open(
            "https://www.youtube.com"
        )


    # --------------------------------------
    # GOOGLE
    # --------------------------------------

    elif "open google" in command:

        speak("Opening Google.")

        webbrowser.open(
            "https://www.google.com"
        )


    # --------------------------------------
    # GOOGLE SEARCH
    # --------------------------------------

    elif "search google for" in command:

        search_text = command.replace(
            "search google for",
            ""
        ).strip()

        if search_text:

            speak(
                "Searching Google for "
                + search_text
            )

            url = (
                "https://www.google.com/search?q="
                + search_text.replace(" ", "+")
            )

            webbrowser.open(url)

        else:

            speak("What should I search for?")


    # --------------------------------------
    # YOUTUBE SEARCH
    # --------------------------------------

    elif "search youtube for" in command:

        search_text = command.replace(
            "search youtube for",
            ""
        ).strip()

        if search_text:

            speak(
                "Searching YouTube for "
                + search_text
            )

            url = (
                "https://www.youtube.com/results?search_query="
                + search_text.replace(" ", "+")
            )

            webbrowser.open(url)

        else:

            speak("What should I search on YouTube?")


    # --------------------------------------
    # EXIT
    # --------------------------------------

    elif (
        "exit" in command
        or "quit" in command
        or "stop" in command
        or "goodbye" in command
    ):

        speak("Goodbye Nikhil!")

        return False


    # --------------------------------------
    # UNKNOWN COMMAND
    # --------------------------------------

    else:

        speak(
            "Sorry Nikhil, I don't know "
            "how to do that yet."
        )


    return True


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    speak(
        "Hello Nikhil. "
        "VoiceMate AI is ready."
    )

    speak(
        "You can say hello, "
        "ask the time, "
        "open YouTube, "
        "or search Google."
    )

    running = True

    while running:

        command = listen()

        running = process_command(command)


# ==========================================
# START
# ==========================================

if __name__ == "__main__":
    main()
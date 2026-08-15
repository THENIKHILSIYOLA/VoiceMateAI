import speech_recognition as sr
import pyttsx3
import webbrowser
import threading
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window


# ==========================================
# VOICEMATE AI
# ==========================================

recognizer = sr.Recognizer()
engine = pyttsx3.init()

engine.setProperty("rate", 170)

Window.size = (400, 700)


# ==========================================
# SPEAK
# ==========================================

def speak(text):

    print("VoiceMate:", text)

    engine.say(text)
    engine.runAndWait()


# ==========================================
# LISTEN
# ==========================================

def listen():

    try:

        with sr.Microphone() as source:

            print("\n🎤 Listening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        text = recognizer.recognize_google(audio)

        text = text.lower()

        print("You said:", text)

        return text

    except sr.WaitTimeoutError:

        print("❌ No voice detected.")

        return ""

    except sr.UnknownValueError:

        print("❌ Could not understand.")

        return ""

    except sr.RequestError:

        print("❌ Speech recognition error.")

        return ""


# ==========================================
# COMMAND PROCESSOR
# ==========================================

def process_command(command):

    if not command:
        return "I could not understand you."

    if "hello" in command or "hi" in command:

        return "Hello Nikhil! How can I help you?"

    elif "what is my name" in command:

        return "Your name is Nikhil."

    elif "time" in command:

        current_time = datetime.now().strftime(
            "%I:%M %p"
        )

        return "The current time is " + current_time

    elif "date" in command:

        current_date = datetime.now().strftime(
            "%d %B %Y"
        )

        return "Today's date is " + current_date

    elif "open youtube" in command:

        webbrowser.open(
            "https://www.youtube.com"
        )

        return "Opening YouTube."

    elif "open google" in command:

        webbrowser.open(
            "https://www.google.com"
        )

        return "Opening Google."

    elif "search google for" in command:

        search_text = command.replace(
            "search google for",
            ""
        ).strip()

        if search_text:

            url = (
                "https://www.google.com/search?q="
                + search_text.replace(" ", "+")
            )

            webbrowser.open(url)

            return (
                "Searching Google for "
                + search_text
            )

        return "What should I search for?"

    elif "search youtube for" in command:

        search_text = command.replace(
            "search youtube for",
            ""
        ).strip()

        if search_text:

            url = (
                "https://www.youtube.com/results?search_query="
                + search_text.replace(" ", "+")
            )

            webbrowser.open(url)

            return (
                "Searching YouTube for "
                + search_text
            )

        return "What should I search on YouTube?"

    elif (
        "exit" in command
        or "stop" in command
        or "goodbye" in command
    ):

        return "Goodbye Nikhil!"

    else:

        return (
            "Sorry Nikhil, I don't know "
            "that command yet."
        )


# ==========================================
# KIVY APP
# ==========================================

class VoiceMateApp(App):

    def build(self):

        self.layout = BoxLayout(
            orientation="vertical",
            padding=25,
            spacing=15
        )

        self.title_label = Label(
            text="🎙️ VoiceMate AI",
            font_size=32,
            size_hint_y=0.15
        )

        self.status_label = Label(
            text="Ready to listen",
            font_size=20,
            size_hint_y=0.15
        )

        self.command_label = Label(
            text="Your command will appear here",
            font_size=18,
            size_hint_y=0.25
        )

        self.mic_button = Button(
            text="🎤\n\nTAP TO SPEAK",
            font_size=24,
            size_hint_y=0.30
        )

        self.mic_button.bind(
            on_press=self.start_listening
        )

        self.history_label = Label(
            text="Command History\n\nNo commands yet",
            font_size=16,
            size_hint_y=0.25
        )

        self.layout.add_widget(
            self.title_label
        )

        self.layout.add_widget(
            self.status_label
        )

        self.layout.add_widget(
            self.command_label
        )

        self.layout.add_widget(
            self.mic_button
        )

        self.layout.add_widget(
            self.history_label
        )

        self.history = []

        return self.layout


    # ======================================
    # START LISTENING
    # ======================================

    def start_listening(self, instance):

        self.status_label.text = "🎤 Listening..."

        self.mic_button.text = (
            "🎤\n\nLISTENING..."
        )

        self.mic_button.disabled = True

        thread = threading.Thread(
            target=self.voice_thread
        )

        thread.daemon = True

        thread.start()


    # ======================================
    # BACKGROUND THREAD
    # ======================================

    def voice_thread(self):

        command = listen()

        Clock.schedule_once(
            lambda dt: self.process_result(command)
        )


    # ======================================
    # PROCESS RESULT
    # ======================================

    def process_result(self, command):

        self.mic_button.disabled = False

        self.mic_button.text = (
            "🎤\n\nTAP TO SPEAK"
        )

        if command:

            self.command_label.text = (
                "You said:\n" + command
            )

            response = process_command(
                command
            )

            self.status_label.text = response

            self.history.append(command)

            self.update_history()

            # Speak in another thread
            threading.Thread(
                target=speak,
                args=(response,),
                daemon=True
            ).start()

        else:

            self.status_label.text = (
                "❌ I couldn't understand."
            )


    # ======================================
    # COMMAND HISTORY
    # ======================================

    def update_history(self):

        recent = self.history[-5:]

        text = "Command History\n\n"

        for command in reversed(recent):

            text += "🎤 " + command + "\n"

        self.history_label.text = text


# ==========================================
# START
# ==========================================

if __name__ == "__main__":

    VoiceMateApp().run()
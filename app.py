import webbrowser
import threading
import subprocess

from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle


# =========================================================
# WINDOW
# =========================================================

Window.size = (400, 700)


# =========================================================
# VOICE FUNCTIONS
# Android-compatible placeholder
# =========================================================

def speak(text):
    """
    Android-safe placeholder.

    pyttsx3 is removed because it is mainly a desktop
    voice engine and can cause Android Buildozer problems.
    """

    print("VoiceMate:", text)


def listen():
    """
    Android-safe placeholder.

    speech_recognition and sr.Microphone() are removed
    from the APK build.

    We will add Android native microphone support later.
    """

    print("Voice input is currently disabled in Android build.")

    return ""


# =========================================================
# COMMAND PROCESSOR
# =========================================================

def process_command(command):

    if not command:
        return "I could not understand you."

    command = command.lower().strip()

    # =====================================================
    # GREETING
    # =====================================================

    if "hello" in command or "hi" in command:

        return "Hello Nikhil! How can I help you?"

    # =====================================================
    # NAME
    # =====================================================

    elif "what is my name" in command:

        return "Your name is Nikhil."

    # =====================================================
    # TIME
    # =====================================================

    elif "time" in command:

        current_time = datetime.now().strftime(
            "%I:%M %p"
        )

        return "The current time is " + current_time

    # =====================================================
    # DATE
    # =====================================================

    elif "date" in command:

        current_date = datetime.now().strftime(
            "%d %B %Y"
        )

        return "Today's date is " + current_date

    # =====================================================
    # OPEN CHROME
    # =====================================================

    elif (
        "open chrome" in command
        or "start chrome" in command
    ):

        try:

            subprocess.Popen(
                "start chrome",
                shell=True
            )

            return "Opening Google Chrome."

        except Exception:

            return "I could not open Chrome."

    # =====================================================
    # SUU PORTAL
    # =====================================================

    elif (
        "open suu portal" in command
        or "open suu" in command
        or "suu portal" in command
        or "open silver oak" in command
    ):

        webbrowser.open(
            "https://www.silveroakuni.ac.in/"
        )

        return "Opening Silver Oak University."

    # =====================================================
    # OPEN YOUTUBE
    # =====================================================

    elif "open youtube" in command:

        webbrowser.open(
            "https://www.youtube.com"
        )

        return "Opening YouTube."

    # =====================================================
    # OPEN GOOGLE
    # =====================================================

    elif "open google" in command:

        webbrowser.open(
            "https://www.google.com"
        )

        return "Opening Google."

    # =====================================================
    # OPEN WHATSAPP
    # =====================================================

    elif (
        "open whatsapp" in command
        or "open whatsapp web" in command
    ):

        webbrowser.open(
            "https://web.whatsapp.com/"
        )

        return "Opening WhatsApp."

    # =====================================================
    # OPEN VS CODE
    # =====================================================

    elif (
        "open vs code" in command
        or "open visual studio code" in command
        or "open code" in command
    ):

        try:

            subprocess.Popen(
                "code",
                shell=True
            )

            return "Opening Visual Studio Code."

        except Exception:

            return "I could not open Visual Studio Code."

    # =====================================================
    # OPEN CALCULATOR
    # =====================================================

    elif (
        "open calculator" in command
        or "open calc" in command
    ):

        try:

            subprocess.Popen(
                "calc",
                shell=True
            )

            return "Opening Calculator."

        except Exception:

            return "I could not open Calculator."

    # =====================================================
    # OPEN NOTEPAD
    # =====================================================

    elif (
        "open notepad" in command
        or "open note pad" in command
    ):

        try:

            subprocess.Popen(
                "notepad",
                shell=True
            )

            return "Opening Notepad."

        except Exception:

            return "I could not open Notepad."

    # =====================================================
    # GOOGLE SEARCH
    # =====================================================

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

    # =====================================================
    # GOOGLE SEARCH SHORT COMMAND
    # =====================================================

    elif "google search" in command:

        search_text = command.replace(
            "google search",
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

    # =====================================================
    # YOUTUBE SEARCH
    # =====================================================

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

    # =====================================================
    # PLAY ON YOUTUBE
    # =====================================================

    elif (
        "play" in command
        and "youtube" in command
    ):

        search_text = command.replace(
            "play",
            ""
        )

        search_text = search_text.replace(
            "on youtube",
            ""
        )

        search_text = search_text.strip()

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

        return "What would you like me to play?"

    # =====================================================
    # EXIT
    # =====================================================

    elif (
        "exit" in command
        or "stop" in command
        or "goodbye" in command
        or "close assistant" in command
    ):

        return "Goodbye Nikhil!"

    # =====================================================
    # UNKNOWN COMMAND
    # =====================================================

    else:

        return (
            "Sorry Nikhil, I don't know "
            "that command yet."
        )


# =========================================================
# ROUNDED BUTTON
# =========================================================

class RoundedButton(Button):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.background_color = (
            0,
            0,
            0,
            0
        )

        with self.canvas.before:

            Color(
                0.12,
                0.35,
                0.95,
                1
            )

            self.background = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[100]
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

    def update_background(self, *args):

        self.background.pos = self.pos
        self.background.size = self.size


# =========================================================
# VOICEMATE APP
# =========================================================

class VoiceMateApp(App):

    # =====================================================
    # BUILD UI
    # =====================================================

    def build(self):

        self.title = "VoiceMate AI"

        self.history = []

        # -------------------------------------------------
        # MAIN LAYOUT
        # -------------------------------------------------

        self.layout = BoxLayout(

            orientation="vertical",

            padding=[
                25,
                25,
                25,
                20
            ],

            spacing=12
        )

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        self.title_label = Label(

            text="VoiceMate AI",

            font_size=30,

            bold=True,

            size_hint_y=0.10
        )

        # -------------------------------------------------
        # GREETING
        # -------------------------------------------------

        current_hour = datetime.now().hour

        if current_hour < 12:

            greeting = "Good Morning"

        elif current_hour < 18:

            greeting = "Good Afternoon"

        else:

            greeting = "Good Evening"

        self.greeting_label = Label(

            text=greeting,

            font_size=21,

            size_hint_y=0.08
        )

        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        self.status_label = Label(

            text="How can I help you?",

            font_size=18,

            size_hint_y=0.10
        )

        # -------------------------------------------------
        # MICROPHONE BUTTON
        # -------------------------------------------------

        self.mic_button = RoundedButton(

            text="MIC\n\nTAP TO SPEAK",

            font_size=22,

            bold=True,

            size_hint_y=0.30
        )

        self.mic_button.bind(

            on_press=self.start_listening

        )

        # -------------------------------------------------
        # COMMAND DISPLAY
        # -------------------------------------------------

        self.command_label = Label(

            text='You said:\n"Nothing yet"',

            font_size=17,

            size_hint_y=0.17
        )

        # -------------------------------------------------
        # HISTORY
        # -------------------------------------------------

        self.history_label = Label(

            text=(
                "Recent Commands\n\n"
                "No commands yet"
            ),

            font_size=15,

            halign="left",

            size_hint_y=0.25
        )

        # -------------------------------------------------
        # ADD WIDGETS
        # -------------------------------------------------

        self.layout.add_widget(
            self.title_label
        )

        self.layout.add_widget(
            self.greeting_label
        )

        self.layout.add_widget(
            self.status_label
        )

        self.layout.add_widget(
            self.mic_button
        )

        self.layout.add_widget(
            self.command_label
        )

        self.layout.add_widget(
            self.history_label
        )

        return self.layout

    # =====================================================
    # START LISTENING
    # =====================================================

    def start_listening(self, instance):

        self.status_label.text = (
            "Listening..."
        )

        self.mic_button.text = (
            "MIC\n\nLISTENING..."
        )

        self.mic_button.disabled = True

        # -------------------------------------------------
        # BACKGROUND THREAD
        # -------------------------------------------------

        thread = threading.Thread(
            target=self.voice_thread
        )

        thread.daemon = True

        thread.start()

    # =====================================================
    # VOICE THREAD
    # =====================================================

    def voice_thread(self):

        command = listen()

        Clock.schedule_once(

            lambda dt:
            self.process_result(command)

        )

    # =====================================================
    # PROCESS RESULT
    # =====================================================

    def process_result(self, command):

        self.mic_button.disabled = False

        self.mic_button.text = (
            "MIC\n\nTAP TO SPEAK"
        )

        if command:

            self.command_label.text = (

                'You said:\n"'
                + command
                + '"'

            )

            # ------------------------------------------------
            # PROCESS COMMAND
            # ------------------------------------------------

            response = process_command(
                command
            )

            # ------------------------------------------------
            # SHOW RESPONSE
            # ------------------------------------------------

            self.status_label.text = response

            # ------------------------------------------------
            # HISTORY
            # ------------------------------------------------

            self.history.append(
                command
            )

            self.update_history()

            # ------------------------------------------------
            # VOICE RESPONSE
            # ------------------------------------------------

            speech_thread = threading.Thread(

                target=speak,

                args=(response,)

            )

            speech_thread.daemon = True

            speech_thread.start()

        else:

            self.status_label.text = (
                "Voice input is not available "
                "in this Android build yet."
            )

    # =====================================================
    # UPDATE HISTORY
    # =====================================================

    def update_history(self):

        recent = self.history[-5:]

        text = (
            "Recent Commands\n\n"
        )

        for command in reversed(recent):

            text += (
                "• "
                + command
                + "\n"
            )

        self.history_label.text = text


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    VoiceMateApp().run()
import webbrowser
import threading

from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle


# =========================================================
# ANDROID IMPORTS
# =========================================================

try:
    from android.permissions import request_permissions, Permission

    ANDROID_AVAILABLE = True

except ImportError:
    ANDROID_AVAILABLE = False


try:
    from jnius import autoclass, PythonJavaClass, java_method

    JNIUS_AVAILABLE = True

except ImportError:
    JNIUS_AVAILABLE = False


# =========================================================
# WINDOW
# =========================================================

Window.size = (400, 700)


# =========================================================
# ANDROID VOICE ENGINE
# =========================================================

speech_text_result = ""


if ANDROID_AVAILABLE and JNIUS_AVAILABLE:

    try:

        PythonActivity = autoclass(
            "org.kivy.android.PythonActivity"
        )

        activity = PythonActivity.mActivity

        TextToSpeech = autoclass(
            "android.speech.tts.TextToSpeech"
        )

        Locale = autoclass(
            "java.util.Locale"
        )

        SpeechRecognizer = autoclass(
            "android.speech.SpeechRecognizer"
        )

        RecognizerIntent = autoclass(
            "android.speech.RecognizerIntent"
        )

        Intent = autoclass(
            "android.content.Intent"
        )

        Bundle = autoclass(
            "android.os.Bundle"
        )

        tts = TextToSpeech(
            activity,
            None
        )

        tts.setLanguage(
            Locale.US
        )

        recognizer = SpeechRecognizer.createSpeechRecognizer(
            activity
        )

        ANDROID_VOICE_READY = True

    except Exception as error:

        print(
            "Android voice initialization error:",
            error
        )

        ANDROID_VOICE_READY = False

else:

    ANDROID_VOICE_READY = False


# =========================================================
# SPEECH LISTENER
# =========================================================

if ANDROID_VOICE_READY:

    class SpeechListener(
        PythonJavaClass
    ):

        __javainterfaces__ = [
            "android/speech/RecognitionListener"
        ]

        def __init__(self, callback):

            super().__init__()

            self.callback = callback


        @java_method("(Landroid/os/Bundle;)V")
        def onReadyForSpeech(self, params):

            print(
                "🎤 Ready for speech"
            )


        @java_method("()V")
        def onBeginningOfSpeech(self):

            print(
                "🎤 Speech started"
            )


        @java_method("(F)V")
        def onRmsChanged(self, rmsdB):

            pass


        @java_method("([B)V")
        def onBufferReceived(self, buffer):

            pass


        @java_method("()V")
        def onEndOfSpeech(self):

            print(
                "🎤 Speech ended"
            )


        @java_method("(I)V")
        def onError(self, error):

            print(
                "Speech recognition error:",
                error
            )

            Clock.schedule_once(
                lambda dt: self.callback("")
            )


        @java_method(
            "(Landroid/os/Bundle;)V"
        )
        def onResults(self, results):

            try:

                matches = results.getStringArrayList(
                    "results_recognition"
                )

                if matches and matches.size() > 0:

                    text = str(
                        matches.get(0)
                    )

                    print(
                        "You said:",
                        text
                    )

                    Clock.schedule_once(
                        lambda dt: self.callback(
                            text.lower()
                        )
                    )

                else:

                    Clock.schedule_once(
                        lambda dt: self.callback("")
                    )

            except Exception as error:

                print(
                    "Result error:",
                    error
                )

                Clock.schedule_once(
                    lambda dt: self.callback("")
                )


        @java_method(
            "(Landroid/os/PartialResults;)V"
        )
        def onPartialResults(self, partial_results):

            pass


        @java_method(
            "(Landroid/os/Bundle;)V"
        )
        def onEvent(self, event_type, params):

            pass


    speech_listener = SpeechListener(
        None
    )

else:

    speech_listener = None


# =========================================================
# SPEAK FUNCTION
# =========================================================

def speak(text):

    print(
        "VoiceMate:",
        text
    )

    if ANDROID_VOICE_READY:

        try:

            tts.speak(
                text,
                TextToSpeech.QUEUE_FLUSH,
                None,
                "VoiceMate"
            )

        except Exception as error:

            print(
                "Android TTS error:",
                error
            )

    else:

        print(
            "Text-to-Speech is available only on Android."
        )


# =========================================================
# LISTEN FUNCTION
# =========================================================

def start_android_listening(callback):

    global speech_listener

    if not ANDROID_VOICE_READY:

        print(
            "Android Speech Recognition unavailable."
        )

        callback("")

        return


    try:

        speech_listener.callback = callback

        recognizer.setRecognitionListener(
            speech_listener
        )

        intent = Intent(
            RecognizerIntent.ACTION_RECOGNIZE_SPEECH
        )

        intent.putExtra(
            RecognizerIntent.EXTRA_LANGUAGE_MODEL,
            RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
        )

        intent.putExtra(
            RecognizerIntent.EXTRA_LANGUAGE,
            "en-IN"
        )

        intent.putExtra(
            RecognizerIntent.EXTRA_MAX_RESULTS,
            5
        )

        recognizer.startListening(
            intent
        )

        print(
            "🎤 Listening..."
        )

    except Exception as error:

        print(
            "Microphone error:",
            error
        )

        callback("")


# =========================================================
# COMMAND PROCESSOR
# =========================================================

def process_command(command):

    if not command:

        return (
            "I could not understand you."
        )


    command = command.lower().strip()


    # =====================================================
    # GREETING
    # =====================================================

    if (
        "hello" in command
        or "hi" in command
    ):

        return (
            "Hello Nikhil! "
            "How can I help you?"
        )


    # =====================================================
    # NAME
    # =====================================================

    elif "what is my name" in command:

        return (
            "Your name is Nikhil."
        )


    # =====================================================
    # TIME
    # =====================================================

    elif "time" in command:

        current_time = datetime.now().strftime(
            "%I:%M %p"
        )

        return (
            "The current time is "
            + current_time
        )


    # =====================================================
    # DATE
    # =====================================================

    elif "date" in command:

        current_date = datetime.now().strftime(
            "%d %B %Y"
        )

        return (
            "Today's date is "
            + current_date
        )


    # =====================================================
    # SILVER OAK UNIVERSITY
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

        return (
            "Opening Silver Oak University."
        )


    # =====================================================
    # OPEN YOUTUBE
    # =====================================================

    elif "open youtube" in command:

        webbrowser.open(
            "https://www.youtube.com"
        )

        return (
            "Opening YouTube."
        )


    # =====================================================
    # OPEN GOOGLE
    # =====================================================

    elif "open google" in command:

        webbrowser.open(
            "https://www.google.com"
        )

        return (
            "Opening Google."
        )


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

        return (
            "Opening WhatsApp."
        )


    # =====================================================
    # OPEN CHROME
    # =====================================================

    elif (
        "open chrome" in command
        or "start chrome" in command
    ):

        webbrowser.open(
            "https://www.google.com"
        )

        return (
            "Opening your browser."
        )


    # =====================================================
    # OPEN VS CODE
    # =====================================================

    elif (
        "open vs code" in command
        or "open visual studio code" in command
        or "open code" in command
    ):

        return (
            "Visual Studio Code cannot be "
            "opened directly from the Android app."
        )


    # =====================================================
    # OPEN CALCULATOR
    # =====================================================

    elif (
        "open calculator" in command
        or "open calc" in command
    ):

        return (
            "Android calculator can be opened "
            "from your phone."
        )


    # =====================================================
    # OPEN NOTEPAD
    # =====================================================

    elif (
        "open notepad" in command
        or "open note pad" in command
    ):

        return (
            "Notepad is not available as a "
            "Windows application on Android."
        )


    # =====================================================
    # GOOGLE SEARCH
    # =====================================================

    elif (
        "search google for" in command
    ):

        search_text = command.replace(
            "search google for",
            ""
        ).strip()


        if search_text:

            url = (
                "https://www.google.com/search?q="
                + search_text.replace(
                    " ",
                    "+"
                )
            )

            webbrowser.open(
                url
            )

            return (
                "Searching Google for "
                + search_text
            )


        return (
            "What should I search for?"
        )


    # =====================================================
    # GOOGLE SEARCH SHORT
    # =====================================================

    elif "google search" in command:

        search_text = command.replace(
            "google search",
            ""
        ).strip()


        if search_text:

            url = (
                "https://www.google.com/search?q="
                + search_text.replace(
                    " ",
                    "+"
                )
            )

            webbrowser.open(
                url
            )

            return (
                "Searching Google for "
                + search_text
            )


        return (
            "What should I search for?"
        )


    # =====================================================
    # YOUTUBE SEARCH
    # =====================================================

    elif (
        "search youtube for" in command
    ):

        search_text = command.replace(
            "search youtube for",
            ""
        ).strip()


        if search_text:

            url = (
                "https://www.youtube.com/results?search_query="
                + search_text.replace(
                    " ",
                    "+"
                )
            )

            webbrowser.open(
                url
            )

            return (
                "Searching YouTube for "
                + search_text
            )


        return (
            "What should I search on YouTube?"
        )


    # =====================================================
    # PLAY YOUTUBE
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
                + search_text.replace(
                    " ",
                    "+"
                )
            )

            webbrowser.open(
                url
            )

            return (
                "Searching YouTube for "
                + search_text
            )


        return (
            "What would you like me to play?"
        )


    # =====================================================
    # EXIT
    # =====================================================

    elif (
        "exit" in command
        or "stop" in command
        or "goodbye" in command
        or "close assistant" in command
    ):

        return (
            "Goodbye Nikhil!"
        )


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

        super().__init__(
            **kwargs
        )

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


    def update_background(
        self,
        *args
    ):

        self.background.pos = (
            self.pos
        )

        self.background.size = (
            self.size
        )


# =========================================================
# VOICEMATE APP
# =========================================================

class VoiceMateApp(App):


    # =====================================================
    # BUILD
    # =====================================================

    def build(self):

        self.title = (
            "VoiceMate AI"
        )

        self.history = []


        # -------------------------------------------------
        # REQUEST ANDROID PERMISSIONS
        # -------------------------------------------------

        if ANDROID_AVAILABLE:

            try:

                request_permissions(
                    [
                        Permission.RECORD_AUDIO,
                        Permission.INTERNET
                    ]
                )

            except Exception as error:

                print(
                    "Permission error:",
                    error
                )


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

        current_hour = (
            datetime.now().hour
        )


        if current_hour < 12:

            greeting = (
                "Good Morning"
            )

        elif current_hour < 18:

            greeting = (
                "Good Afternoon"
            )

        else:

            greeting = (
                "Good Evening"
            )


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

    def start_listening(
        self,
        instance
    ):

        self.status_label.text = (
            "Listening..."
        )

        self.mic_button.text = (
            "MIC\n\nLISTENING..."
        )

        self.mic_button.disabled = True


        if ANDROID_VOICE_READY:

            thread = threading.Thread(

                target=self.android_voice_thread

            )

            thread.daemon = True

            thread.start()

        else:

            self.process_result("")


    # =====================================================
    # ANDROID VOICE THREAD
    # =====================================================

    def android_voice_thread(self):

        try:

            start_android_listening(
                self.process_result
            )

        except Exception as error:

            print(
                "Voice thread error:",
                error
            )

            Clock.schedule_once(
                lambda dt: self.process_result("")
            )


    # =====================================================
    # PROCESS RESULT
    # =====================================================

    def process_result(
        self,
        command
    ):

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


            # ---------------------------------------------
            # PROCESS COMMAND
            # ---------------------------------------------

            response = process_command(
                command
            )


            # ---------------------------------------------
            # SHOW RESPONSE
            # ---------------------------------------------

            self.status_label.text = (
                response
            )


            # ---------------------------------------------
            # HISTORY
            # ---------------------------------------------

            self.history.append(
                command
            )


            self.update_history()


            # ---------------------------------------------
            # VOICE RESPONSE
            # ---------------------------------------------

            speech_thread = threading.Thread(

                target=speak,

                args=(response,)

            )

            speech_thread.daemon = True

            speech_thread.start()


        else:

            self.status_label.text = (
                "I couldn't understand."
            )


    # =====================================================
    # UPDATE HISTORY
    # =====================================================

    def update_history(self):

        recent = (
            self.history[-5:]
        )


        text = (
            "Recent Commands\n\n"
        )


        for command in reversed(
            recent
        ):

            text += (
                "• "
                + command
                + "\n"
            )


        self.history_label.text = (
            text
        )


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    VoiceMateApp().run()
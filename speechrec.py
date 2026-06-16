import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import pyttsx3
import speech_recognition as sr

# Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

class SpeechTherapyApp(App):

    def build(self):
        self.layout = BoxLayout(
            orientation='vertical',
            padding=10,
            spacing=10
        )

        self.instructions = Label(
            text="Enter a word you want to practice:"
        )
        self.layout.add_widget(self.instructions)

        self.word_input = TextInput(
            hint_text="Type word to practice"
        )
        self.layout.add_widget(self.word_input)

        self.feedback_label = Label(
            text="Feedback will appear here."
        )
        self.layout.add_widget(self.feedback_label)

        self.start_button = Button(
            text="Start Practice"
        )
        self.start_button.bind(on_press=self.start_practice)
        self.layout.add_widget(self.start_button)

        return self.layout

    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    def start_practice(self, instance):
        word_to_practice = self.word_input.text.strip()

        if word_to_practice:
            self.speak(f"Please say the word {word_to_practice}")
            self.feedback_label.text = (
                f"Please say the word: {word_to_practice}"
            )

            result = self.recognize_speech(word_to_practice)
            self.feedback_label.text = result
        else:
            self.feedback_label.text = "Please enter a word first."

    def recognize_speech(self, word_to_practice):
        recognizer = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                self.feedback_label.text = "Listening..."
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            recognized_word = recognizer.recognize_google(audio).lower()

            if recognized_word == word_to_practice.lower():
                return (
                    f"Well done! You said "
                    f"'{recognized_word}' correctly."
                )
            else:
                return (
                    f"Oops! You said "
                    f"'{recognized_word}'. Try again."
                )

        except sr.UnknownValueError:
            return "Could not understand audio."

        except sr.RequestError:
            return "Speech recognition service error."

        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    SpeechTherapyApp().run()
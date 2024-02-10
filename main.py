import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os

# Initialize the pyttsx3 engine for text-to-speech
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty(
    "voice", voices[1].id
)  # You can change the index to 1 for a different voice


def speak(audio):
    """Function to speak the given audio"""
    engine.say(audio)
    engine.runAndWait()


def wish_me():
    """Function to wish the user based on the time of the day"""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Tanvir 2.0, your personal assistant. How may I assist you?")


def take_command():
    """Function to take voice input from the user and return the recognized text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't understand that. Can you please repeat?")
        return "None"
    return query


if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command().lower()

        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "open youtube" in query:
            webbrowser.open("youtube.com")
        elif "open google" in query:
            webbrowser.open("google.com")
        elif "open facebook" in query:
            webbrowser.open("facebook.com")

        elif "play music" in query:
            music_dir = "D:\\programming\\python\\jarvis2.0\\Music"  # Update this with your music directory
            songs = os.listdir(music_dir)
            os.startfile(
                os.path.join(music_dir, songs[0])
            )  # Play the first song in the directory

        elif "the time" in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {str_time}")

        elif "open vs" in query:
            code_path = (
                "C:\\Users\\Lenovo\\AppData\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code.exe"  # Update this with your VSCode path
            )
            os.startfile(code_path)
        elif "tanveer" in query:
            speak("I am Tanvir 2.0, your personal assistant. How may I assist you?")  

        elif "exit" in query:
            speak("Goodbye Sir!")
            break

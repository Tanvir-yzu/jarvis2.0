import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import requests

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


# Function to fetch the current weather
def get_weather():
    url = "https://open-weather13.p.rapidapi.com/city/Yangzhou,%20Jiangsu"
    headers = {
        "X-RapidAPI-Key": "b1bd08449amsh47a3ca09da73cedp1a828fjsn5a1506014af8",
        "X-RapidAPI-Host": "open-weather13.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if "main" in data and "temp" in data["main"] and "weather" in data:
            temperature = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"]
            return f"The current temperature in Yangzhou City,  is {temperature} degrees Celsius with {weather_desc}."
        else:
            return "Sorry, weather information is not available."
    else:
        return "Sorry, I couldn't fetch the weather information."


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
        elif "the date" in query:
            str_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Sir, today's date is {str_date}")
        elif "weather" in query:
            weather_info = get_weather()
            speak(weather_info)

        elif "open vs" in query:
            code_path = "C:\\Users\\Lenovo\\AppData\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code.exe"  # Update this with your VSCode path
            os.startfile(code_path)

        elif "tanveer" in query:
            speak("I am Tanvir 2.0, your personal assistant. How may I assist you?")
        elif "how are you" in query:
            speak("I'm doing well, thank you!")
        elif "hello" in query:
            speak("Hello! How can I assist you?")

        elif "goodbye" in query or "exit" in query:
            speak("Goodbye Sir!")
            break

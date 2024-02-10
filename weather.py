import speech_recognition as sr
import pyttsx3
import datetime
import os
import psutil

# Initialize the speech recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak out the response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to the user's command
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
    except sr.UnknownValueError:
        command = ""
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    return command

# Function to play music
def play_music():
    music_dir = "D:\\programming\\python\\jarvis2.0\\Music"  # Update this with your music directory
    songs = os.listdir(music_dir)
    os.startfile(os.path.join(music_dir, songs[0]))

# Function to close music playback
def close_music():
    for proc in psutil.process_iter():
        if "wmplayer.exe" in proc.name():  # Adjust for your media player process name
            proc.terminate()
            speak("Music playback stopped.")
            break
    else:
        speak("No music is currently playing.")

# Main function to handle commands
def main():
    speak("Hello, I am Tanvir 2.0, your personal assistant. How may I assist you?")
    while True:
        query = listen()

        if "hello" in query:
            speak("Hello! How can I assist you?")
        elif "how are you" in query:
            speak("I'm doing well, thank you!")
        elif "what's your name" in query:
            speak("I am Tanvir 2.0, your personal assistant.")
        elif "the time" in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {str_time}")
        elif "the date" in query:
            str_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Sir, today's date is {str_date}")
        elif "play music" in query:
            play_music()
        elif "stop music" in query or "close music" in query:
            close_music()
        elif "goodbye" in query or "exit" in query:
            speak("Goodbye! Have a great day!")
            break
        else:
            speak("I'm sorry, I didn't understand that command.")

if __name__ == "__main__":
    main()

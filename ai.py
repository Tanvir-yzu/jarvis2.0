import sys
import warnings
import tinydb
import pyttsx3
import speech_recognition as sr
from whisper import WhisperModel
from transformers import pipeline

# Load the Whisper model
tiny_model = WhisperModel.from_pretrained("whisper-model")

# Load the GPT4All model
base_model = pipeline("text2text", model="gpt4all-base")

# Define the wake word
wake_word = "hey gpt4all"

# Initialize the listening mode
listening_for_wake_word = True

# Initialize the microphone
source = sr.Microphone()
 
# Filter warnings
warnings.filterwarnings("ignore", category=UserWarning, module='whisper.transcribe', lineno=114)

# Initialize the text-to-speech engine
if sys.platform != 'darwin':
    engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    if sys.platform == 'darwin':
        ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!-_$:+-/ ")
        clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
        system(f"say '{clean_text}'")
    else:
        engine.say(text)
        engine.runAndWait()

# Function to listen for the wake word
def listen_for_wake_word(audio):
    global listening_for_wake_word
    with open("wake_detect.wav", "wb") as f:
        f.write(audio.get_wav_data())
    result = tiny_model.transcribe('wake_detect.wav')
    text_input = result['text']
    if wake_word in text_input.lower().strip():
        print("Wake word detected. Please speak your prompt to GPT4All.")
        speak('Listening')
        listening_for_wake_word = False

# Function to listen for a prompt and generate a response
def prompt_gpt(audio):
    global listening_for_wake_word
    try:
        with open("prompt.wav", "wb") as f:
            f.write(audio.get_wav_data())
        result = base_model.transcribe('prompt.wav')
        prompt_text = result['text']
        if len(prompt_text.strip()) == 0:
            print("Empty prompt. Please speak again.")
        else:
            response = base_model(prompt_text)
            speak(response['generated_text'])
            listening_for_wake_word = True
    except Exception as e:
        print(f"Error: {e}")
        listening_for_wake_word = True

# Main loop
while True:
    if listening_for_wake_word:
        with source as s:
            audio = s.listen(timeout=5)
            listen_for_wake_word(audio)
    else:
        with source as s:
            audio = s.listen(timeout=5)
            prompt_gpt(audio)
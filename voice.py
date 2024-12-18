import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import pywhatkit as kit
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Access system audio settings
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, 
    1, 
    None
)
volume = interface.QueryInterface(IAudioEndpointVolume)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            # Adding a timeout of 5 seconds
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            talk("Sorry, I could not understand. Can you repeat?")
            return None
        except sr.RequestError:
            talk("Sorry, the service is down. Please try again later.")
            return None
        except sr.WaitTimeoutError:
            talk("I didn't hear anything. Please say something.")
            return None

def execute_command(command):
    if 'open' in command:
        if 'chrome' in command:
            talk("Opening Google Chrome.")
            os.system("start chrome")
        elif 'notepad' in command:
            talk("Opening Notepad.")
            os.system("notepad")
        elif 'calculator' in command:
            talk("Opening Calculator.")
            os.system("calc")
        else:
            talk("Sorry, I cannot open that application.")
    
    elif 'play' in command:
        song = command.replace("play", "")
        talk(f"Playing {song}")
        kit.playonyt(song)
    
    elif 'search' in command:
        search_query = command.replace("search", "")
        talk(f"Searching for {search_query} on Google.")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
    
    elif 'raise volume' in command:
        current_volume = volume.GetMasterVolumeLevelScalar()
        if current_volume < 1.0:
            new_volume = min(current_volume + 0.1, 1.0)
            volume.SetMasterVolumeLevelScalar(new_volume, None)
            talk("Raising the volume.")
        else:
            talk("The volume is already at the maximum level.")
    
    elif 'lower volume' in command:
        current_volume = volume.GetMasterVolumeLevelScalar()
        if current_volume > 0.0:
            new_volume = max(current_volume - 0.1, 0.0)
            volume.SetMasterVolumeLevelScalar(new_volume, None)
            talk("Lowering the volume.")
        else:
            talk("The volume is already at the minimum level.")
    
    elif 'close' in command:
        if 'chrome' in command:
            talk("Closing Google Chrome.")
            os.system("taskkill /f /im chrome.exe")
        elif 'notepad' in command:
            talk("Closing Notepad.")
            os.system("taskkill /f /im notepad.exe")
        elif 'calculator' in command:
            talk("Closing Calculator.")
            os.system("taskkill /f /im calc.exe")
        else:
            talk("Sorry, I cannot close that application.")
    
    elif 'exit' in command or 'quit' in command:
        talk("Goodbye.")
        exit()

def main():
    talk("Hello, how can I assist you today?")
    while True:
        command = listen()
        if command:
            execute_command(command)

if __name__ == "__main__":
    main()

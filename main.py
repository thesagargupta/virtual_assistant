import webbrowser
import speech_recognition as sr
import pyttsx3
import musiclibrary
import requests
import threading
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Spotify configuration
SPOTIPY_CLIENT_ID = 'CONFIDENTIAL'
SPOTIPY_CLIENT_SECRET = 'CONFIDENTIAL'
SPOTIPY_REDIRECT_URI = 'CONFIDENTIAL'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-read-playback-state,user-modify-playback-state'))

# Speech engine configuration
recognizer = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
for voice in voices:
    if 'zira' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 135)  # Slightly faster
engine.setProperty('volume', 1.0)

# Flag to control speaking state
speaking = False

def speak(text):
    """ Speak the given text and ensure the assistant can continue processing commands. """
    global speaking
    if not speaking:
        speaking = True
        engine.say(text)
        engine.runAndWait()
        speaking = False

def get_coordinates(city):
    """ Fetch latitude and longitude for a given city """
    api_key = "CONFIDENTIAL"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]
            return lat, lon
        else:
            speak(f"Sorry, I couldn't find coordinates for {city}.")
            return None
    except Exception as e:
        speak("An error occurred while fetching coordinates.")
        print(e)
        return None

def get_weather(city):
    """ Fetch and speak the current weather for a given city """
    coordinates = get_coordinates(city)
    if coordinates:
        lat, lon = coordinates
        api_key = "CONFIDENTIAL"  # Replace with your OpenWeatherMap API key
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url)
            weather_data = response.json()
            if weather_data["cod"] == 200:
                main = weather_data["main"]
                weather = weather_data["weather"][0]
                temp = main["temp"]
                description = weather["description"]
                speak(f"The current temperature in {city} is {temp} degrees Celsius with {description}.")
            else:
                speak(f"Sorry, I couldn't find the weather information for {city}.")
        except Exception as e:
            speak("An error occurred while fetching the weather.")
            print(e)

def get_news():
    """ Fetch and speak the latest news headlines """
    api_key = "CONFIDENTIAL"  # Replace with your NewsAPI key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"

    try:
        response = requests.get(url)
        news_data = response.json()
        if news_data["status"] == "ok":
            headlines = [article["title"] for article in news_data["articles"][:5]]
            speak("Here are the latest headlines:")
            for headline in headlines:
                speak(headline)
                print(headline)
        else:
            speak("Sorry, I couldn't fetch the news headlines.")
    except Exception as e:
        speak("An error occurred while fetching the news.")
        print(e)


def play_song(command):
    """ Play song either from the custom library or Spotify """
    song_name = command.lower().replace("play song", "").strip()
    
    # First, try to check in the custom music library
    if song_name in musiclibrary.music:
        url = musiclibrary.music[song_name]
        print(f"Playing {song_name} from your music library...")
        webbrowser.open(url)
        speak(f"Playing {song_name} from your music library.")
    else:
        # Search for the song on Spotify if not found in library
        def search_on_spotify():
            print(f"Searching for '{song_name}' on Spotify...")
            results = sp.search(q=song_name, type='track', limit=3)  # Limit the results for quicker response
            tracks = results['tracks']['items']

            if tracks:
                track = tracks[0]
                spotify_url = track['external_urls']['spotify']
                print(f"Found: {track['name']} by {track['artists'][0]['name']}. Opening in Spotify...")
                webbrowser.open(spotify_url)
                speak(f"Opening {track['name']} by {track['artists'][0]['name']} in Spotify.")
            else:
                speak(f"Sorry, I couldn't find {song_name} on Spotify.")
                print("No tracks found.")

        # Run Spotify search in a separate thread for faster response
        threading.Thread(target=search_on_spotify).start()

def listen_for_command():
    """ Capture user voice input and respond """
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Faster noise adjustment
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)  # Reduced time limits
            print("Captured audio, recognizing...")
            recognized_command = recognizer.recognize_google(audio)
            print(f"Recognized Command: {recognized_command}")  # Debugging output
            return recognized_command
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None
        except sr.UnknownValueError:
            print("Sorry, I did not understand that. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

def processCommand(c):
    """ Process different user commands """
    print(f"Processing command: {c}")  # Debugging output
    if c.lower() == "open google":
        webbrowser.open("https://www.google.com/")
    elif c.lower() == "open youtube":
        webbrowser.open("https://www.youtube.com/")
    elif c.lower() == "open instagram":
        webbrowser.open("https://www.instagram.com/")
    elif "play song" in c.lower() or "play" in c.lower():  # Adjusted to recognize variations
        play_song(c)
    elif "she is angry" in c.lower() or "angry with me" in c.lower():
        speak("Play a song for her...")
        play_song("for her")  # Play a predefined calming song
    elif "sagar gupta" in c.lower() or "sagar" in c.lower():
        speak("sagar gupta is a famous personality, holding skills of many programming languages, he is MILLIONAIRE")
        print("sagar gupta is a famous personality, holding skills of many programming languages, he is MILLIONAIRE")
        speak("a song is dedicated to sagar's personality,")
        play_song("for sagar")

    elif "weather" in c.lower() or "temperature" in c.lower():  # Fixed typo "temprature"
        if "in" in c.lower():
            city = c.lower().split("in")[-1].strip()
            speak(f"Fetching weather information for {city}.")
            get_weather(city)
        elif "for" in c.lower():
            city = c.lower().split("for")[-1].strip()
            speak(f"Fetching weather information for {city}.")
            get_weather(city)
        else:
            speak("Please specify a city for the weather.")
    elif "news" in c.lower() or "headlines" in c.lower() or "headline" in c.lower():
        speak("Fetching the latest news headlines.")
        get_news()
    else:
        speak("Sorry, I didn't understand that.")



if __name__ == '__main__':
    speak("Hello, I'm Anu. How may I assist you?")

    activated = False  # Track activation state
    while True:
        if not activated:  # Only listen for activation commands when not activated
            word = listen_for_command()
            if word:
                print(f"Recognized: {word}")
                if word.lower().startswith(("hello", "hi", "hey")):
                    speak("Aha! How can I help you?")
                    activated = True  # Set activated state

        if activated:  # Continue listening for commands
            command = listen_for_command()
            if command:
                print(f"Command: {command}")
                if command.lower() in ["exit", "stop"]:
                    speak("Goodbye!")
                    activated = False  # Exit the activated state
                else:
                    processCommand(command)



import webbrowser
import speech_recognition as sr
import pyttsx3
import musiclibrary
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import threading

# Spotify configuration
SPOTIPY_CLIENT_ID = '9a7fbadb8fc34f3ea487b3887f944f44'
SPOTIPY_CLIENT_SECRET = 'af9db1b03d024315a10141c95c23d4e4'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

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

# Flag to control pyttsx3 speaking state
speaking = False

def speak(text):
    """ Speak the given text """
    global speaking
    if not speaking:
        speaking = True
        engine.say(text)
        engine.runAndWait()
        speaking = False

def get_coordinates(city):
    """ Fetch latitude and longitude for a given city """
    api_key = "2546b20f2e5b3f647a3ad38cbfcea4e4"  # Replace with your OpenWeatherMap API key
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
        api_key = "2546b20f2e5b3f647a3ad38cbfcea4e4"  # Replace with your OpenWeatherMap API key
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
    api_key = "aa93a1da17d942ff8a0df9dda1ef1638"  # Replace with your NewsAPI key
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
        # Search for the song on Spotify
        def search_on_spotify():
            print(f"Searching for {song_name} on Spotify...")
            results = sp.search(q=song_name, type='track')
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

def processCommand(c):
    """ Process different user commands """
    if c.lower() == "open google":
        webbrowser.open("https://www.google.com/")
    elif c.lower() == "open youtube":
        webbrowser.open("https://www.youtube.com/")
    elif c.lower() == "open instagram":
        webbrowser.open("https://www.instagram.com/")
    elif c.lower().startswith("play"):
        play_song(c)
    elif "weather" in c.lower():
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

def listen_for_command():
    """ Capture user voice input and respond """
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Faster noise adjustment
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)  # Reduced time limits
            print("Captured audio, recognizing...")
            return recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None

if __name__ == '__main__':
    speak("Hello, I'm Anu. How may I assist you?")

    while True:
        try:
            word = listen_for_command()
            if word:
                print(f"Recognized: {word}")

                if word.lower().startswith(("hello", "hi", "hey")):
                    speak("Aha")
                    command = listen_for_command()
                    if command:
                        print(f"Command: {command}")
                        processCommand(command)

        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"Error: {e}")
            speak("An error occurred.")

import webbrowser
import speech_recognition as sr
import pyttsx3
import musiclibrary
import requests  
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
SPOTIPY_CLIENT_ID = '9a7fbadb8fc34f3ea487b3887f944f44'
SPOTIPY_CLIENT_SECRET = 'af9db1b03d024315a10141c95c23d4e4'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-read-playback-state,user-modify-playback-state'))

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set voice properties (Zira voice)
voices = engine.getProperty('voices')
for voice in voices:
    if 'zira' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 130)
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def play_song(command):
    song_name = command.lower().replace("play song", "").strip()

    if song_name in musiclibrary.music:
        url = musiclibrary.music[song_name]
        print(f"Playing {song_name} from your music library...")
        webbrowser.open(url)
        speak(f"Playing {song_name} from your music library.")
    else:
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

def get_weather(city):
    api_key = "2546b20f2e5b3f647a3ad38cbfcea4e4"  # Replace with your actual OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        weather_data = response.json()
        
        if weather_data["cod"] == 200:
            main = weather_data["main"]
            weather = weather_data["weather"][0]
            temp = main["temp"]
            description = weather["description"]
            speak(f"The current temperature in {city} is {temp} degrees Celsius with {description}.")
            print(f"Weather in {city}: {temp}°C, {description}.")
        else:
            speak(f"Sorry, I couldn't find the weather information for {city}.")
            print(f"Error message from API: {weather_data.get('message')}")
    except Exception as e:
        speak("An error occurred while fetching the weather.")
        print(e)

def get_news():
    api_key = "aa93a1da17d942ff8a0df9dda1ef1638"  # Replace with your actual news API key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        news_data = response.json()
        
        if news_data["status"] == "ok":
            articles = news_data["articles"]
            headlines = [article["title"] for article in articles[:5]]  # Get top 5 headlines
            
            for headline in headlines:
                speak(headline)
                print(headline)
        else:
            speak("Sorry, I couldn't fetch the news at the moment.")
    except Exception as e:
        speak("An error occurred while fetching the news.")
        print(e)

def process_command(command):
    if "open google" in command.lower():
        webbrowser.open("https://www.google.com/")
    elif "open youtube" in command.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open instagram" in command.lower():
        webbrowser.open("https://www.instagram.com/")
    elif "play" in command.lower():
        play_song(command)
    elif "weather" in command.lower():
        city = command.split("in")[-1].strip() if "in" in command.lower() else command.split("for")[-1].strip()
        speak(f"Fetching weather information for {city}.")
        get_weather(city)
    elif "news" in command.lower():
        speak("Fetching today's headlines.")
        get_news()
    else:
        speak("Sorry, I didn't understand that.")

def listen_for_command():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        return audio

if __name__ == '__main__':
    speak("Hello, I'm Anu. How may I assist you?")
    while True:
        try:
            audio = listen_for_command()
            print("Captured audio, recognizing...")
            word = recognizer.recognize_google(audio, language="hi-IN")  # Change this to "en-US" for English
            
            print(f"Recognized: {word}")
            process_command(word)
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"Error: {e}")
            speak("An error occurred.")

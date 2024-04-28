import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import pywhatkit
import pyjokes
import requests
import json
from twilio.rest import Client
import openai

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning Aman!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Aman!")
    else:
        speak("Good Evening Aman!")

    speak("I am Jarvis. How may I help you?")


def takecommand():
    # It takes microphone input and returns as string
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("LISTENING...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("You said:", query)

    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your password')  # Replace with your email and password
    server.sendmail('yourmail@gmail.com', to, content)
    server.close()


def make_call(number):
    # Twilio credentials
    account_sid = 'YOUR_ACCOUNT_SID'  # Replace with your Twilio account SID
    auth_token = 'YOUR_AUTH_TOKEN'  # Replace with your Twilio authentication token
    twilio_number = 'YOUR_TWILIO_PHONE_NUMBER'  # Replace with your Twilio phone number

    client = Client(account_sid, auth_token)

    call = client.calls.create(
        to=number,
        from_=twilio_number,
        url='http://demo.twilio.com/docs/voice.xml'  # URL with TwiML instructions for the call
    )

    print(call.sid)


def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)


def get_weather():
    api_key = "YOUR_API_KEY"  # Replace with your API key from OpenWeatherMap
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = "YOUR_CITY_NAME"  # Replace with your city name
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"] - 273.15  # Convert to Celsius
        weather_desc = data["weather"][0]["description"]
        speak(f"The temperature in {city_name} is {temperature:.2f} degrees Celsius with {weather_desc}.")
    else:
        speak("City not found.")


def suggest_movies():
    api_key = 'YOUR_TMDB_API_KEY'  # Replace with your TMDB API key
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data['results'][:5]  # Get top 5 popular movies
        for movie in results:
            title = movie['title']
            speak(f"I suggest you watch {title}.")
    else:
        speak("Sorry, I couldn't fetch movie suggestions at the moment.")


def get_opinion(topic):
    openai.api_key = 'YOUR_OPENAI_API_KEY'  # Replace with your OpenAI API key
    prompt = f"What's your opinion on {topic}?"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=50
    )
    opinion = response.choices[0].text.strip()
    speak(opinion)


if __name__ == "__main__":
    wishme()
    while True:
        query = takecommand().lower()

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("https://www.stackoverflow.com")

        elif 'play music' in query:
            mus = 'x:\\music'
            songs = os.listdir(mus)
            print(songs)
            os.startfile(os.path.join(mus, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Bro, the time is {strTime}")

        elif 'open code' in query:
            codepath = "C:\\Users\\Aman\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codepath)

        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = takecommand()
                to = "receivermail@gmail.com"  # Replace with the recipient's email address
                sendEmail(to, content)
                speak("Email has been sent.")

            except Exception as e:
                print(e)
                speak("Sorry bro, I am not able to send this email")

        elif 'make a call' in query:
            speak("Whom do you want to call?")
            contact = takecommand()
            make_call(contact)

        elif 'tell a joke' in query:
            tell_joke()

        elif 'weather today' in query:
            get_weather()

        elif 'suggest movies' in query:
            suggest_movies()

        elif 'opinion on' in query:
            topic = query.replace("opinion on", "").strip()
            get_opinion(topic)

        elif 'stop jarvis' in query:
            speak("Ok, Nice helping you, Bye")
            exit()

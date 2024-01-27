import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib

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
    server.login('youremail@gmail.com', 'your password')
    server.sendmail('yourmail@gmail.com', to, content)
    server.close()


if __name__ == "__main__":
    wishme()
    while True:
        query = takecommand().lower()

        # Logic for executing tasks based on query
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

        elif 'stop jarvis' in query:
            speak("Ok, Nice helping you, Bye")
            exit()

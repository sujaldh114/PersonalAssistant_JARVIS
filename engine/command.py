import pyttsx3
import speech_recognition as sr
import eel
import time
from engine.config import API_KEY
from engine.gemini_api import ask_gemini


# ---------- TEXT-TO-SPEECH ----------
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 175)
    engine.say(text)
    engine.runAndWait()


# ---------- VOICE RECOGNITION ----------
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        eel.DisplayMessage("Listening...")

        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)

    try:
        print("🧠 Recognizing...")
        eel.DisplayMessage("Recognizing...")

        query = r.recognize_google(audio, language='en-in').lower()
        print(f"User said: {query}")

        # 🔹 Hotword detection skip
        if any(hw in query for hw in ["jarvis", "alexa"]):
            print("🔥 Hotword detected! Triggering mic from Python...")
            eel.triggerMicFromPython()
            return ""

        eel.DisplayMessage(f"You said: {query}")
        return query

    except Exception as e:
        print("❌ Could not understand:", e)
        eel.DisplayMessage("Sorry, I couldn't understand.")
        return ""



## ---------- COMMON COMMAND HANDLER ----------

def handle_query(query):
    query = query.lower().strip()

    if not query:
        return "Sorry, I didn't catch that."

    try:
        from engine.features import openCommand, PlayYoutube

        # 1. Play YouTube videos
        if "play" in query and "youtube" in query:
            PlayYoutube(query)
            return "Playing your requested video on YouTube."

        # 2. Open YouTube
        elif "open youtube" in query or query == "youtube":
            import webbrowser
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube."

        # 3. Open WhatsApp
        elif "open whatsapp" in query or query == "whatsapp":
            import webbrowser
            webbrowser.open("https://web.whatsapp.com")
            return "Opening WhatsApp."

        # 4. Open other applications
        elif query.startswith("open "):
            success = openCommand(query)

            if success:
                return "Opening " + query.replace("open ", "").strip()

            return "Sorry, I couldn't open that application."

        # 5. WhatsApp messaging and calling
        elif any(x in query for x in [
            "send message", "phone call", "video call"
        ]):
            from engine.features import findContact, whatsApp

            contact_no, name = findContact(query)

            if contact_no != 0:
                if "send message" in query:
                    speak("What message should I send?")
                    message = takecommand()
                    if not message:
                        return "Message cancelled."

                    whatsApp(contact_no, message, "message", name)

                elif "phone call" in query:
                    whatsApp(contact_no, "", "call", name)

                else:
                    whatsApp(contact_no, "", "video call", name)

                return "WhatsApp action completed for " + name

            return "Contact not found."

        # 6. General AI questions
        else:
            response = ask_gemini(query)
            speak(response)
            return response

    except Exception as e:
        print("Command error:", e)
        return "Sorry, something went wrong."


# ---------- VOICE COMMANDS ----------

@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
    else:
        query = message

    response = handle_query(query)

    print("JARVIS:", response)

    eel.DisplayMessage(response)

    return response


# ---------- TEXT COMMANDS ----------

@eel.expose
def textCommand(message):

    print("Text command:", message)

    response = handle_query(message)

    print("JARVIS:", response)

    return response
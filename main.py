import os
import threading
import eel
import time
from engine.features import *
from engine.command import *


def start():
    eel.init("www")

    playAssistantSound()

    # Open the web app
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    # Start hotword detection thread
    threading.Thread(target=hotword_listener, daemon=True).start()

    # Start Eel server
    eel.start('index.html', mode=None, host='localhost')


def hotword_listener():
    import pvporcupine
    import pyaudio
    import struct

    porcupine = None
    paud = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("🎧 Hotword listener started. Say 'Jarvis' or 'Alexa'...")

        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:
                print("🎙️ Hotword detected! Activating mic...")

                try:
                    eel.triggerMicFromPython()
                    print("✅ Microphone trigger sent to frontend")

                except Exception as e:
                    print("❌ Mic trigger error:", e)

                time.sleep(2)

    except Exception as e:
        print(f"❌ Error in hotword listener: {e}")

    finally:
        if porcupine:
            porcupine.delete()
        if audio_stream:
            audio_stream.close()
        if paud:
            paud.terminate()


if __name__ == "__main__":
    start()

# PersonalAssistant_JARVIS

JARVIS is a Windows voice assistant with a web interface, hotword detection,
application launching, YouTube playback, WhatsApp actions, and Gemini AI
responses.

## Setup

1. Create and activate a Python environment.
2. Install the project dependencies used by the `engine` modules.
3. Copy `.env.example` to `.env` and set `GEMINI_API_KEY`.
4. Restore your local `contacts.csv` and `jarvis.db` files if you use contact
   actions. They are intentionally excluded from Git because they contain
   personal data.
5. Run `python main.py`.

The `envjarvis` virtual environment, local database, contacts, API keys, and
personal project documents are excluded from version control.

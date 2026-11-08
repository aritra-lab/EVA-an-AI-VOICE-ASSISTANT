
# EVA — Enhanced Virtual Assistant

EVA is a personal assistant project with two parts: a Python backend in the `EVA` folder and a Flutter user interface in the sibling `eva_flutter` folder. The backend listens for spoken commands, speaks its replies, and manages common desktop tasks, notes, reminders, and saved information. The Flutter frontend provides a chat interface and microphone control that communicate with the backend over its local HTTP API. Commands are matched by EVA's local command router first; unmatched questions are sent to the Groq-powered conversational assistant.

## Features

- **Voice interaction:** Uses your microphone to recognize commands and speaks replies aloud with an English (India) neural voice.
- **Conversation and help:** Answers general questions through the Groq API; responds to greetings and can describe its command capabilities.
- **Apps and browser:** Opens supported Windows apps and websites, closes supported processes, searches Google or YouTube, and controls browser tabs.
- **Tasks:** Adds tasks with optional due dates and high/normal/low priority, lists all or pending tasks, and completes or deletes tasks by ID or keyword. EVA announces due and overdue tasks on startup.
- **Notes:** Saves, lists, and deletes notes by ID or matching text.
- **Memory:** Stores simple key/value facts, recalls them, lists saved memories, and forgets facts.
- **WhatsApp helpers:** Opens WhatsApp Web, saves and lists contacts, opens a contact chat, and prepares a message draft. Message preparation copies the draft to the clipboard for you to review and send manually.
- **System and media:** Reports system information and battery status, takes screenshots, reads or changes volume, and reports weather for a city.
- **Camera:** Takes a selfie, detects faces in a camera frame, and recognizes the configured owner using the existing face profile/model.
- **Power controls:** Locks or sleeps the computer; shutdown and restart require voice confirmation.
- **Optional local HTTP API:** `api_server.py` exposes chat, speech, listening, and startup summary endpoints for a local client such as the companion Flutter app.

## Requirements

- Windows 10/11 (several app, audio, volume, and power integrations are Windows-specific).
- Python 3.10 or newer recommended.
- A working microphone and speakers/headphones. A webcam is needed for camera commands.
- Internet access for speech recognition, text-to-speech, weather, and the AI fallback.
- A Groq API key for the conversational fallback.

## Installation

Open PowerShell in the project directory and create/activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Install the Python packages used by the project:

```powershell
python -m pip install groq python-dotenv edge-tts pygame SpeechRecognition PyAudio opencv-contrib-python psutil pyperclip pyautogui pycaw comtypes requests numpy
```

`opencv-contrib-python` supplies the `cv2.face` recognizer used for owner recognition. If PyAudio installation fails, install a wheel compatible with your Python version and Windows architecture, then retry the command.

Create a `.env` file in the project root and add your Groq key:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Keep the key private; do not commit `.env` to a public repository. The weather integration currently uses an API key configured in `modules/weather.py`.

## Run EVA

From the `EVA` backend folder, start the standalone voice assistant:

```powershell
python MAIN.py
```

EVA greets you and then listens continuously. Speak a command after it prints that it is listening. If no command is recognized, it waits again. Say **“goodbye”** or **“bye”** to exit the assistant. (The phrase **“shut down”** by itself is also treated as exiting EVA; use the explicit “shut down the computer” phrase to request a PC shutdown.)

To run only the optional local API server instead:

```powershell
python api_server.py
```

It listens on `http://127.0.0.1:5000`. Keep it local; the server binds only to loopback.

## Frontend and backend setup

The project folders are siblings:

```text
Desktop/
├── EVA/          # Python backend and local HTTP API
└── eva_flutter/  # Flutter desktop/mobile/web client
```

### Python backend (`EVA/MAIN.py`)

`MAIN.py` is the standalone, continuously listening assistant. It registers the command handlers, greets the user, announces task reminders and startup counts, then listens through the microphone. Use `python MAIN.py` when you want to use EVA by voice directly from the computer.

For the Flutter application, start the backend API from the `EVA` directory instead:

```powershell
python api_server.py
```

The API server loads the same command router and Groq fallback for the frontend. It listens on `127.0.0.1:5000`; leave this terminal running while using the Flutter app. Avoid running `MAIN.py` at the same time as the API when both are using the same microphone/audio devices.

### Flutter frontend (`eva_flutter/lib/main.dart`)

The Flutter app entry point builds the EVA Material app and opens the home screen. The current interface includes:

- **Chat:** Type a message and submit it to the backend; user and EVA replies appear in the conversation.
- **Voice control:** Tap the microphone to ask the backend to listen once. The recognized phrase is then sent through the chat endpoint as a command.
- **Startup greeting and summary:** On launch, the frontend requests a greeting, speaks it using the backend, fetches database counts/reminders, and displays and speaks the available startup summary.
- **Settings navigation:** A Settings page is present as a placeholder and currently displays “WORK IN PROGRESS...”.

The Flutter client uses `lib/services/eva_api.dart` to call the backend's `/chat`, `/listen`, `/startup`, and `/speak` endpoints. The configured base URL is `http://127.0.0.1:5000`.

To run the Flutter app, open a second PowerShell terminal in `eva_flutter` after starting `api_server.py`:

```powershell
flutter pub get
flutter run -d windows
```

Flutter SDK is required in addition to the Python dependencies. `pubspec.yaml` currently requires Dart SDK `^3.12.2`. The project also contains Android, iOS, macOS, Linux, and web targets, but the API URL and backend integrations are designed for a local computer setup. On an Android emulator, `127.0.0.1` points to the emulator itself; use an emulator-to-host address or configure `EvaApi.baseUrl` and backend binding/network settings for that target. Physical devices likewise need a reachable backend address. Keep the backend private and do not expose it to an untrusted network.

## Commands and examples

EVA uses phrase matching, so these examples show supported wording. You can speak them or send them to the `/chat` API.

| Capability | Example commands |
|---|---|
| Help and conversation | “What can you do?”, “Who are you?”, or ask a general question |
| Open or close apps | “Open calculator”, “Open WhatsApp”, “Close notepad” |
| Search and tabs | “Search for space news”, “Search YouTube for jazz”, “Open a new tab”, “Next tab”, “Close tab” |
| Time and date | “Tell me the time”, “What is the date?” |
| Weather | “Weather in Kolkata”, “What is the temperature in London?” |
| Tasks | “Add task submit report tomorrow high priority”, “Show my tasks”, “Show pending tasks”, “Complete task 2”, “Delete task report” |
| Notes | “Take note buy groceries”, “Show notes”, “Delete note 1” |
| Saved memories | “Remember my favorite color is blue”, “Recall my favorite color”, “Show memories”, “Forget my favorite color” |
| Volume | “Mute”, “Unmute”, “Increase volume by 10”, “Decrease volume by 5”, “Set volume to 40 percent”, “What is the volume?” |
| System | “System information”, “Battery status”, “Take a screenshot” |
| Camera | “Take selfie”, “Detect face”, “Recognize me” |
| WhatsApp | “Open WhatsApp”, “Add WhatsApp contact”, “Show WhatsApp contacts”, “Open WhatsApp chat”, “Message Alex saying I will be late” |
| Power | “Lock the computer”, “Sleep computer”, “Restart the computer”, “Shut down the computer” |

For task completion or deletion, EVA accepts a task ID or a keyword. WhatsApp contact management and chat selection use console prompts. The smart message flow displays the recipient and message for confirmation, opens the chat, then copies the draft; send it yourself in WhatsApp after reviewing it.

## Local API

All request and response bodies use JSON. For example:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/chat `
  -ContentType 'application/json' `
  -Body '{"message":"What time is it?"}'
```

| Method and path | Purpose |
|---|---|
| `GET /` | Check that the API is online |
| `GET /startup` | Get status plus note, task, due-today, and overdue counts |
| `POST /chat` | Send `{"message":"..."}` through the existing command router, then AI fallback if no command matches; returns `reply` and `handled` |
| `POST /listen` | Listen through the microphone and return a recognized `command`; it does not execute that command |
| `POST /speak` | Speak `{"message":"..."}` aloud |

Invalid/empty JSON messages receive an error response. The API is a local integration interface, not an authenticated remote service; do not expose it to an untrusted network.

## Data and project layout

- `MAIN.py` — starts EVA, registers command handlers, and runs the microphone loop.
- `api_server.py` — optional local HTTP API.
- `core/` — command routing, speech, startup reminders, and command handlers.
- `modules/` — desktop integrations and data operations.
- `config.py` — recognized command phrases and application aliases.
- `eva.db` — SQLite database for tasks, notes, memories, and WhatsApp contacts.
- `data/` — face detector and owner face profile/model.
- `logs/` — runtime logs.
- `photos/` — selfies are saved here when the directory is created by the camera module.

The database and face data are stored locally in the project. Back up `eva.db` and any face profile you want to keep. Avoid publishing personal data, face images, model files, logs, or API credentials.

## Troubleshooting

- **Microphone or recognition problems:** Check Windows microphone permissions and the default recording device. Speech recognition uses Google's online recognition service, so internet access is required.
- **No spoken response / audio initialization error:** Check the Windows output device and verify the audio dependencies (`pygame`, `edge-tts`) are installed.
- **AI fallback errors:** Check that `.env` is in the project root, `GROQ_API_KEY` is set, and the machine can reach Groq.
- **Camera commands fail:** Check webcam permissions and ensure another program is not occupying the camera. Owner recognition also requires a compatible OpenCV contrib build and a trained model in `data/face_profiles/owner/`.
- **An app does not open:** App launching depends on Windows and, for Office applications, the paths configured in `modules/apps.py`.
- **PowerShell blocks venv activation:** You may run `\.venv\Scripts\python.exe MAIN.py` without activating the environment, or adjust the execution policy for your user if appropriate.

## Notes

- The exact phrases shown above correspond to current phrase matching in the code; command recognition may vary with the speech recognizer.
- Shutdown and restart operate on the current computer after confirmation. Use these commands only when you intend to close your session.
- The application keeps short conversational context in memory while running. Persistent task, note, contact, and saved-memory records are kept in SQLite.
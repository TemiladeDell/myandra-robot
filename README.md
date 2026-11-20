# Myandra

Myandra is a voice-interactive educational robot built as a final-year project. It combines a Raspberry Pi camera and a browser-based animated face with a voice assistant and an Arduino-connected drive system.

The joystick page lets an operator drive the robot and record a question. Faster Whisper transcribes the recording. Myandra combines the transcript with recent conversation and saved facts, then asks an Ollama-hosted Qwen model for a response. Edge TTS turns the response into audio, and the face page displays the answer and plays the generated speech. The camera is used for face recognition and for updating the animated eyes.

| Component | Role |
| --- | --- |
| `main.py` | Starts the face display, joystick and eye tracker, then runs the conversation loop |
| `face.py` | Serves the animated face and displays generated answers |
| `joystick.py` | Serves the driving and recording controls, and sends commands over serial |
| `face_manager.py`, `eye_tracker.py` | Identify saved profiles and update eye direction |
| `context_builder.py`, `model_manager.py` | Build the conversation context and request a reply from Ollama |
| `myandradb_link.py`, `schema.sql` | Initialize and store profiles, conversation history, facts and face file references |

## Hardware and software

- Raspberry Pi running Raspberry Pi OS, with a Picamera2-compatible camera and an ALSA microphone.
- Arduino with matching motor firmware. The Python controller sends newline-terminated `FORWARD`, `BACKWARD`, `LEFT`, `RIGHT` and `STOP` commands at 9600 baud. Arduino firmware and wiring diagrams are outside this source release.
- A browser for the face display and joystick and a speaker for audio.
- Ollama on the Pi or a reachable computer with the `qwen2.5:1.5b` model installed.

## Setup

Run these commands from the repository root on the Pi. The virtual environment includes system packages so it can access Picamera2 and OpenCV from Raspberry Pi OS.

```sh
sudo apt update
sudo apt install python3-venv python3-picamera2 python3-opencv cmake build-essential python3-dev portaudio19-dev alsa-utils mpg123
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On the computer running Ollama, download the model with `ollama pull qwen2.5:1.5b` and make sure Ollama is running. On the Pi, set the following environment variables as needed. Use `arecord -l` to find the microphone card and device numbers.

| Variable | Default or purpose |
| --- | --- |
| `OLLAMA_HOST` | `http://localhost:11434`. Set it to the Ollama server address for a remote model. |
| `MYANDRA_SERIAL_PORT` | `/dev/ttyACM0` |
| `MYANDRA_AUDIO_DEVICE` | `plughw:3,0` |
| `TAVILY_API_KEY` | Optional key for Tavily web lookups. Keep the value in your shell environment. |

Run `python main.py` from the repository root. The database is created automatically. The first transcription may need network access to download the Faster Whisper model. Speech synthesis uses Edge TTS and requires internet access.

- Open `http://<pi-address>:5001` for the face display.
- Open `http://<pi-address>:5000` for the joystick and recording controls.
- The Flask servers listen on the local network, and the joystick has no login. Run the robot on a trusted network.

## Face profiles

A fresh database starts with no enrolled faces. The conversation loop creates a guest profile for an unrecognized visitor. Face enrollment is available through `face_manager.register_face(user_id)` for an existing profile. Run enrollment with permission from the person being enrolled and with the camera free. Face encodings, conversations and microphone recordings are stored locally and ignored by Git.

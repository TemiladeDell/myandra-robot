# Myandra

**Mobile Intelligent Companion Educator (M.I.C.E.)** · Final-year project

I built Myandra as a mobile, non-humanoid educational companion that could hold a spoken conversation, remember useful information, recognise returning users, and interact through a physical robot. I used a Raspberry Pi 4, an Arduino Uno and a Samsung S10 to bring those pieces together.

[Build process](#build-process) · [Hardware](#hardware) · [Source guide](#source-guide) · [Setup](#setup) · [What I would improve](#what-i-would-improve)

## Build process

### Defining the companion and choosing a model

I started with the kind of interaction I wanted a learner to have. I gave the companion the name **Myandra** and used **M.I.C.E.** as the project title. That distinction mattered when writing the system prompt. Clear instructions about the robot's name, educational role and tone gave the model a more consistent role to play across interactions.

I chose an existing Qwen model served through Ollama. That gave me a way to focus on how the robot would behave and what information it would have at each turn. Training changes the model's parameters. A system prompt guides the response during inference, and application memory gives the model information retrieved from outside it. I could change Myandra's role or give it a fact from an earlier conversation without retraining Qwen.

### Setting up the Pi and connecting it to Ollama

I used a Raspberry Pi 4 with 4 GB of RAM running Raspberry Pi OS based on Debian 13 (Trixie). I developed from my Windows laptop over SSH, which let me work on the robot without attaching a keyboard and monitor each time. The Pi handled the camera, microphone, database, web interfaces and serial control. My laptop served the language model over the local network.

That division taught me to check where a service was running, which address and port it listened on, and whether the other device could reach it. When Ollama was unreachable, I could test its API from the Pi with `curl http://<ollama-host>:11434/api/tags` before changing the Python code. I also learned to check which Python interpreter was running. A missing `tavily` import turned out to be a matter of activating my project virtual environment, where the package was already installed.

### Building conversation memory and deciding what to send

I used SQLite to keep data across restarts. Profiles, learning records, conversation history, known facts and face file references each had their own table. That gave me practice with SQL queries, primary keys and using user IDs to associate information across tables.

The running conversation loop supplies recent dialogue, available profile and learning data, and saved facts to the prompt builder. A separate keyword-based history retriever was another approach I explored for finding older conversations. I also added optional Tavily search so the context builder could bring in outside information for suitable questions. The search path uses simple rules to skip some personal questions and follow-ups.

I learned to treat saving information and choosing what to send to the model as separate decisions. A database can hold a long conversation history. The answer still depends on whether the application selects the parts that help with the current question.

### Giving Myandra a face, a voice and a camera

I used Flask to serve two browser interfaces. The animated face runs on port 5001, and the joystick and recording controls run on port 5000. Reusing a Samsung S10 as the face display let me work with the hardware I already had.

Pressing the recording control captures audio through the USB microphone on the Pi. Faster Whisper transcribes it, the conversation loop sends the resulting prompt to Ollama, and Edge TTS generates an MP3 from the reply. Getting sound to the phone was a separate problem from generating the audio. I served the MP3 through Flask and had the browser check for a new file before playing it. That taught me to trace which device produces the file and which device is responsible for playback.

The Raspberry Pi Camera Module 3 supported another input path. I used face encodings to look for a registered user and a separate eye tracker to update the direction of the animated eyes. This gave me a practical way to see how computer vision and language processing could share a robot while doing different jobs.

### Moving from browser input to physical motion

I split control between the Raspberry Pi and the Arduino Uno. The browser joystick sends a direction to Flask. The Pi relays it over serial, and the Arduino handles the lower-level motor control through an L298N driver and DC TT motors. Keeping movement in that path gave me a clear boundary between the conversation system and the motor controller.

Working with an ultrasonic sensor, cliff sensors and a servo introduced me to GPIO, distance readings and the physical constraints around movement. I also learned to account for current draw when motors start or a servo is under load. A motor command can be correct in software while the robot still behaves unreliably because of its power supply, common ground, wiring or mechanical load.

I explored Autodesk Fusion 360 and 3D printing while figuring out how to mount the parts. Designing around component sizes, cable routes, weight distribution and manufacturing tolerances made me think about how the robot would actually fit together and move.

### Integrating and troubleshooting the prototype

I split the Python code into modules for speech, model requests, context, storage and hardware interaction. The main process coordinates the conversation and starts separate processes for the face, joystick and eye tracking. Managing those processes taught me to think about which component owns each resource, how components exchange updates and what happens when one of them stops.

My most useful troubleshooting habit was to test each boundary on its own. For a silent reply, I could check whether a recording existed, whether transcription returned text, whether Ollama produced a reply, whether the MP3 was generated and whether the intended browser received it. For a networking problem, I could check the service from the Pi directly. For a movement problem, I could trace the command from the joystick through serial and then check the motor electronics and power.

## Hardware

| Component | Role in the build |
| --- | --- |
| Raspberry Pi 4 (4 GB) | Runs the Python application and coordinates the peripherals |
| Arduino Uno, L298N driver and DC TT motors | Drive control and movement |
| Raspberry Pi Camera Module 3 | Face recognition and eye tracking |
| USB microphone | Records spoken questions |
| Samsung S10 | Browser display and audio playback |
| Ultrasonic sensor and cliff sensors | Distance and edge sensing explored during development |
| MG995 servo | Controlled rotation explored during development |
| Speaker and MAX98357A amplifier | Dedicated audio output considered during development |

The Python controller expects matching Arduino firmware and sends newline-terminated `FORWARD`, `BACKWARD`, `LEFT`, `RIGHT` and `STOP` commands at 9600 baud. Arduino firmware and wiring diagrams are outside this source release.

## Source guide

| Component | Role |
| --- | --- |
| [`main.py`](main.py) | Starts supporting processes and runs the conversation loop |
| [`face.py`](face.py), [`joystick.py`](joystick.py) | Serve the animated face, audio, recording and movement controls |
| [`face_manager.py`](face_manager.py), [`eye_tracker.py`](eye_tracker.py) | Match enrolled faces and update eye direction |
| [`speech_to_text.py`](speech_to_text.py), [`text_to_speech.py`](text_to_speech.py) | Convert recorded speech to text and generate reply audio |
| [`context_builder.py`](context_builder.py), [`system_prompt_builder.py`](system_prompt_builder.py), [`model_manager.py`](model_manager.py) | Assemble context and instructions, then request a reply from Ollama |
| [`myandradb_link.py`](myandradb_link.py), [`schema.sql`](schema.sql) | Initialize and persist local data |
| [`memory_retriever.py`](memory_retriever.py), [`web_search.py`](web_search.py) | Implement keyword-based history retrieval and optional external lookup |

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

## What I would improve

- **Conversation.** Improve memory selection, test identity consistency over longer conversations and compare models for latency and quality on available hardware.
- **Voice and vision.** Improve recognition in noisy settings, make audio playback more responsive, and evaluate more reliable face recognition and offline options.
- **Movement and hardware.** Develop obstacle avoidance and autonomous navigation, then improve power distribution, battery operation, component mounting and chassis durability.
- **Reliability and privacy.** Improve logging, testing and process recovery, and add stronger controls around the joystick, saved conversations and face data.

## Final reflection

Building Myandra changed how I think about AI products. The model generated the language, but the experience a person had with the robot also depended on what I gave the model to work with, how the answer reached the person, and how reliably the hardware and software worked together. The project taught me to design those connections and to trace problems across them, from a prompt or database query all the way to a browser, camera or motor.

from Conversation_manager import greet_user
from context_builder import build_context
from system_prompt_builder import build_system_prompt
from model_manager import generate_response
from myandradb_link import save_message, initialize_user_session, load_user
from memory_extractor import extract_memory
import os
from speech_to_text import transcribe_audio
from text_to_speech import speak_text
import sys
import time
from Conversation_manager import extract_name
from user_manager import create_user
from face_manager import identify_user, register_face
import subprocess
from user_manager import create_guest_user

subprocess.Popen([sys.executable, "face.py"])
time.sleep(3)




awaiting_name = False

user_id = identify_user()
print("IDENTIFIED USER =", user_id)

subprocess.Popen([sys.executable,"joystick.py"])

if user_id:
    initialize_user_session(user_id)


if user_id:
    profile = load_user(user_id)
    name = profile["name"] if profile else ""
    greeting = f"Welcome back, {name}." if name else "Welcome back."
else:
    greeting = "Hello. I don't think we've met before."
subprocess.Popen([sys.executable, "eye_tracker.py"])

if user_id is None:
    awaiting_name = True

print(greeting)



if os.path.exists("response.mp3"):
    os.remove("response.mp3")
speak_text(greeting)

#os.system("mpg123 -q response.mp3")

while True:

    if not os.path.exists("talk.txt"):
        time.sleep(0.2)
        continue

    os.remove("talk.txt")
    print("Processing...")

    message = transcribe_audio("test.wav")

    if awaiting_name:

        name = extract_name(message)

        user_id = create_guest_user()
        initialize_user_session(user_id)

        print(f"Nice to meet you")
        welcome = f"Nice to meet you. How can I help you today?"

        print(welcome)

        speak_text(welcome)

        #os.system("mpg123 -q response.mp3")

        awaiting_name = False

        continue

    if len(message.strip()) < 3:
        print("Didn't catch that. Try again.")
        continue

    print(f"\nYou: {message}")

    extract_memory(
        user_id,
        message
    )

    if message.lower() == "exit":
        break

    save_message(user_id, "user", message)

    context = build_context(
    user_id,
    message
    )


    system_prompt = build_system_prompt(context)

    llm_start = time.time()

    response = generate_response(
       system_prompt,
       message
    )

    print(
       "LLM:",
       time.time() - llm_start
    )
    response = response.strip()
    with open("teaching.txt", "w") as f:
        f.write(response)

    if "." in response:
        response = response[:response.rfind(".") + 1]

    save_message(user_id, "assistant", response)

    print(response)

    speak_text(response)
    os.system("mpg123 response.mp3")

    end = time.time()

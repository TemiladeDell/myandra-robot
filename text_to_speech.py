import asyncio
import edge_tts
import time

VOICE = "en-US-JennyNeural"

PRONUNCIATIONS = {
    "Temilade": "taymi laa day",
    "Myandra": "miandra"
}

async def speak(text):

    for word, replacement in PRONUNCIATIONS.items():
        text = text.replace(word, replacement)

    communicate = edge_tts.Communicate(
        text,
        VOICE
    )

    await communicate.save("response.mp3")


def speak_text(text):

    tts_start = time.time()

    asyncio.run(
        speak(text)
    )

    print(
        "TTS:",
        time.time() - tts_start
    )

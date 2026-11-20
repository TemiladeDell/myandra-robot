from faster_whisper import WhisperModel

model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

def transcribe_audio(audio_file):

    segments, info = model.transcribe(
    audio_file,
    language="en"
)

    text = ""

    for segment in segments:
        text += segment.text + " "

    return text.strip()

    stt_start = time.time()

    message = transcribe_audio("test.wav")

    print(
       "STT:",
       time.time() - stt_start
    )

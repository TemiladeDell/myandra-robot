import collections
import wave
import pyaudio
import webrtcvad

RATE = 48000
CHANNELS = 1
FRAME_DURATION = 30
FRAME_SIZE = int(RATE * FRAME_DURATION / 1000)



vad = webrtcvad.Vad(2)

audio = pyaudio.PyAudio()

stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=RATE,
    input=True,
    input_device_index=1,
    frames_per_buffer=1440
)

print("Listening...")

frames = []

speech_started = False
silence_frames = 0

while True:

    frame = stream.read(
        FRAME_SIZE,
        exception_on_overflow=False
    )

    is_speech = vad.is_speech(
        frame,
        RATE
    )

    if is_speech:

        speech_started = True
        silence_frames = 0
        frames.append(frame)

    elif speech_started:

        frames.append(frame)
        silence_frames += 1

        if silence_frames > 30:
            break

stream.stop_stream()
stream.close()
audio.terminate()

with wave.open("test.wav", "wb") as wf:

    wf.setnchannels(CHANNELS)

    wf.setsampwidth(
        pyaudio.get_sample_size(
            pyaudio.paInt16
        )
    )

    wf.setframerate(RATE)

    wf.writeframes(
        b"".join(frames)
    )

print("Recording complete")

import speech_recognition as sr
import sounddevice as sd
import io
import wave

SAMPLE_RATE = 16000
CHUNK_DURATION = 3

def recognize_once():
    r = sr.Recognizer()
    audio_data = sd.rec(int(CHUNK_DURATION * SAMPLE_RATE),
                        samplerate=SAMPLE_RATE,
                        channels=1, dtype='int16')
    sd.wait()

    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())
    wav_buffer.seek(0)

    with sr.AudioFile(wav_buffer) as source:
        audio = r.record(source)

    return r.recognize_google(audio)
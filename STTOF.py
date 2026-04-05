import sounddevice as sd
import vosk
import json
import queue
import sys
import time
from contextlib import contextmanager

SAMPLE_RATE = 16000
BLOCK_SIZE = 8000
VOSK_MODEL_PATH = "model"

print("Loading Vosk model...")
_model = vosk.Model(VOSK_MODEL_PATH)
print("Vosk ready ✅")

_q = queue.Queue()

def _callback(indata, frames, time_info, status):
    if status:
        print(f"[Vosk Warning]: {status}", file=sys.stderr)
    _q.put(bytes(indata))

@contextmanager
def get_stream():
    stream = sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        dtype='int16',
        channels=1,
        callback=_callback,
        device=5
    )
    stream.start()
    try:
        yield stream
    finally:
        stream.stop()
        stream.close()

def recognize_once():
    recognizer = vosk.KaldiRecognizer(_model, SAMPLE_RATE)
    start = time.time()

    while time.time() - start < 6:
        try:
            chunk = _q.get(timeout=0.5)
            if recognizer.AcceptWaveform(chunk):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()
                if text:
                    return text
        except queue.Empty:
            continue

    final = json.loads(recognizer.FinalResult())
    text = final.get("text", "").strip()
    return text if text else None
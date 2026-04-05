import urllib.request
import time
import speech_recognition as sr

import STTON
import STTOF

# ─────────────────────────────────────────
# INTERNET CHECK
# ─────────────────────────────────────────
def is_internet_available():
    try:
        urllib.request.urlopen("http://google.com", timeout=2)
        return True
    except Exception:

        return False

# ─────────────────────────────────────────
# MAIN MANAGER
# ─────────────────────────────────────────
def run():
    print("\n🎙️ ALEX STT Manager Started")
    print("Say 'stop' to exit | Ctrl+C to force quit\n")

    current_mode = None

    with STTOF.get_stream():
        while True:
            try:
                # ── CHECK INTERNET FIRST ──
                internet = is_internet_available()
                new_mode = "ONLINE" if internet else "OFFLINE"

                # ── MODE SWITCH NOTIFICATION ──
                if new_mode != current_mode:
                    current_mode = new_mode
                    if current_mode == "ONLINE":
                        print("\n🌐 [Switched → ONLINE | Google STT]")
                    else:
                        print("\n📴 [Switched → OFFLINE | Vosk STT]")

                # ── ONLINE MODE ──
                if current_mode == "ONLINE":
                    try:
                        text = STTON.recognize_once()
                    except sr.UnknownValueError:
                        print("...")
                        continue
                    except sr.RequestError:
                        # Force switch immediately
                        print("⚠️ Internet lost! Switching to Vosk...")
                        current_mode = "OFFLINE"
                        text = STTOF.recognize_once()

                # ── OFFLINE MODE ──
                else:
                    text = STTOF.recognize_once()
                    if not text:
                        continue

                # ── OUTPUT ──
                if text:
                    print(f"[{current_mode}] You said: {text}")
                    if "stop" in text.lower():
                        print("🛑 Stopping...")
                        break

            except KeyboardInterrupt:
                print("\n👋 Stopped.")
                break
            except Exception as e:
                print(f"[Error]: {e}")
                time.sleep(1)
                continue

if __name__ == "__main__":
    run()
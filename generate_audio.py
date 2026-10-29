#!/usr/bin/env python3
"""Generate the natural Spanish audio the study guide plays.

The site plays pre-recorded clips from audio/ (listed in audio/manifest.json)
instead of the browser's built-in voice. This script reads every Spanish word,
expression and grammar example straight out of index.html, so there is no list
to maintain and nothing to paste back.

WHEN TO RUN IT: after adding a lesson or examples to index.html.

HOW TO RUN IT (from this folder):
    export ELEVEN_API_KEY='sk_your_key_here'
    python3 generate_audio.py

Existing clips are skipped, so re-running only fetches new text (cheap).
Use another voice with VOICE_ID='...' python3 generate_audio.py
Preview what would be generated without a key: python3 generate_audio.py --list
"""
import hashlib, json, os, subprocess, sys, time, urllib.request, urllib.error

# Fix the common macOS "certificate verify failed" error automatically.
try:
    import certifi
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "audio")
MODEL = "eleven_multilingual_v2"


def spanish_strings():
    """Evaluate the content arrays in index.html with node and collect every spoken string."""
    html = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
    start, end = html.index("const LESSONS"), html.index("const CHANNELS")
    js = html[start:end] + """
      const out = [
        ...LESSONS.flatMap(l => l.words.map(w => w.es)),
        ...GRAMMAR.flatMap(g => g.examples.map(e => e[0])),
      ];
      console.log(JSON.stringify([...new Set(out)]));
    """
    res = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


words = spanish_strings()
if "--list" in sys.argv:
    print("\n".join(words)); print(f"\n{len(words)} strings"); sys.exit()

API = os.environ.get("ELEVEN_API_KEY", "").strip()
env_file = os.path.join(HERE, ".env")  # git-ignored
if not API and os.path.exists(env_file):
    for line in open(env_file, encoding="utf-8"):
        if line.startswith("ELEVEN_API_KEY="):
            API = line.split("=", 1)[1].strip().strip("'\"")
if not API and sys.stdin.isatty():
    import getpass
    API = getpass.getpass("Paste your ElevenLabs API key (hidden), then press Return: ").strip()
if not API:
    sys.exit("ERROR: set ELEVEN_API_KEY first, e.g.  export ELEVEN_API_KEY='sk_...'")

# Built-in premade voice (usable by any account; needs only TTS permission).
vid = os.environ.get("VOICE_ID", "EXAVITQu4vr4xnSDxMaL")  # Sarah
os.makedirs(OUT_DIR, exist_ok=True)
print(f"Voice {vid}  model={MODEL}\nGenerating {len(words)} clips into audio/ ...")


def tts(text, path):
    body = json.dumps({
        "text": text,
        "model_id": MODEL,
        "voice_settings": {"stability": 0.55, "similarity_boost": 0.8, "style": 0.0, "use_speaker_boost": True},
    }).encode("utf-8")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
    req = urllib.request.Request(url, data=body, method="POST",
        headers={"xi-api-key": API, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    with urllib.request.urlopen(req, timeout=60) as r:
        audio = r.read()
    with open(path, "wb") as f:
        f.write(audio)
    return len(audio)


manifest, fails = {}, []
for i, text in enumerate(words, 1):
    # Voice is part of the hash so switching VOICE_ID regenerates everything.
    fname = hashlib.md5(f"{vid}|{text}".encode("utf-8")).hexdigest()[:16] + ".mp3"
    path = os.path.join(OUT_DIR, fname)
    manifest[text] = fname
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print(f"  [{i:2}/{len(words)}] skip  {text}")
        continue
    for attempt in range(4):
        try:
            n = tts(text, path)
            print(f"  [{i:2}/{len(words)}] ok    {text} ({n}B)")
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:200]
            print(f"  [{i:2}/{len(words)}] HTTP {e.code} attempt {attempt+1}: {msg}")
            if e.code in (401, 403):
                sys.exit("Auth failed — check the API key.")
            time.sleep(3 * (attempt + 1))
        except Exception as e:
            print(f"  [{i:2}/{len(words)}] err attempt {attempt+1}: {e}")
            time.sleep(3 * (attempt + 1))
    else:
        del manifest[text]; fails.append(text)

with open(os.path.join(OUT_DIR, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)

# Remove clips that no longer match any text (old voice, edited examples).
keep = set(manifest.values()) | {"manifest.json"}
stale = [f for f in os.listdir(OUT_DIR) if f not in keep]
for f in stale:
    os.remove(os.path.join(OUT_DIR, f))

print(f"\nDone. {len(manifest)} clips. Removed {len(stale)} stale. Failures: {fails or 'none'}")

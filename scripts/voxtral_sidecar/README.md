# Voxtral Sidecar — TTS/ASR HTTP wrapper

[Voxtral](https://github.com/nihilistau/voxtral-mini-realtime-rs) is a pure-Rust
**CLI** for text-to-speech and speech-to-text. It has **no HTTP server**, so this
sidecar wraps the built `voxtral` binary as a tiny HTTP service whose contract
matches the game's existing clients — `engine/media/tts.py` (port **8600**) and
`engine/media/stt.py` (port **5051**) — so nothing in the game changes.

## Contract (what the game expects)

**TTS** — `POST /tts` (or whatever `tts.base_url` + path the client uses):
```
request:  { "text": "<narration>", "voice": "grey_wanderer", "style": "whisper" }
response: audio/wav  (24 kHz)   OR   { "audio_url": "/media/<id>.wav" }
```
Maps to: `voxtral speak --text "..." --voice <preset> --gguf models/voxtral-tts-q4.gguf`

**ASR** — `POST /asr` (player push-to-talk; the scene already posts to
`/api/voice/transcribe`):
```
request:  multipart audio file (16 kHz mono wav)
response: { "text": "<transcript>" }
```
Maps to: `voxtral transcribe --audio in.wav --gguf models/voxtral-asr-q4.gguf`

## Implementation sketch (FastAPI, ~60 lines)

A minimal `sidecar.py` that:
1. Receives `/tts` JSON → writes nothing, shells `voxtral speak ...` → returns the wav.
2. Receives `/asr` multipart → saves to a temp wav → shells `voxtral transcribe ...`
   → returns `{ "text": stdout.strip() }`.
3. Reads `VOXTRAL_BIN`, `VOXTRAL_TTS_GGUF`, `VOXTRAL_ASR_GGUF` from env.

Voice presets (20 across 9 languages) map to our Assistant forms / Storyteller
voice styles. The realtime WASM build is an alternative for in-browser streaming.

## Graceful degradation

If the sidecar is down or `tts.fallback: text` is set, the game shows narration
as text and skips audio — no crash. This sidecar is **optional** and runs on the
GPU "beast"; on a CPU-only box leave it off.

See `knowledge/runbooks/install-voxtral.md`.

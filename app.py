from flask import Flask, request, send_file, jsonify
import requests
import tempfile
import os

app = Flask(__name__)

# Set your ElevenLabs API Key and Voice ID
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "ELEVENLABS_API_KEY")
VOICE_ID = "21m00Tcm4TlvDq8ikWAM" # Rachel (default)

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Text is required"}), 400

    print(f"🔊 Requesting voice for text: {text}")

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    response = requests.post(url, headers=headers, json=payload, stream=True)

    print("🧪 Status code:", response.status_code)
    print("🔁 Response text:", response.text)


    if response.status_code != 200:
        print("❌ Error response:", response.text)
        return jsonify({"error": "Failed to generate voice", "details": response.text}), 500

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                tmp_file.write(chunk)
        tmp_file_path = tmp_file.name

    print(f"✅ MP3 saved to {tmp_file_path}")
    return send_file(tmp_file_path, mimetype="audio/mpeg")

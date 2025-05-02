
from flask import Flask, request, send_file, jsonify
import requests
import tempfile
import os

app = Flask(__name__)

# 🔐 Replace with your ElevenLabs API key
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "your_api_key_here")
VOICE_ID = "your_voice_id_here"  # Replace with your chosen ElevenLabs voice ID

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Text is required"}), 400

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

    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    response = requests.post(tts_url, headers=headers, json=payload, stream=True)

    if response.status_code != 200:
        return jsonify({"error": "Failed to generate audio"}), 500

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                tmp_file.write(chunk)
        tmp_file_path = tmp_file.name

    return send_file(tmp_file_path, mimetype="audio/mpeg", as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

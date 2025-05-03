# app.py — AI Voice Backend with ElevenLabs + Health Check
from flask import Flask, request, send_file, jsonify
import requests
import tempfile
import os

app = Flask(__name__)

# Load API key and voice ID from environment variables
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = os.environ.get("VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Default to Rachel

@app.route("/", methods=["GET"])
def health():
    return "✅ AI Voice backend is running! Use POST /speak to synthesize."

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Text is required"}), 400

    print(f"🔊 Requesting speech for: {text}")

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

    try:
        response = requests.post(url, headers=headers, json=payload, stream=True, timeout=20)
        print("🧪 Status code:", response.status_code)

        if response.status_code != 200:
            print("❌ Error text:", response.text)
            return jsonify({"error": "Failed to generate audio", "details": response.text}), 500

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    tmp_file.write(chunk)
            tmp_file_path = tmp_file.name

        print(f"✅ MP3 saved to {tmp_file_path}")
        return send_file(tmp_file_path, mimetype="audio/mpeg")

    except requests.exceptions.RequestException as e:
        print("❌ Exception during API request:", str(e))
        return jsonify({"error": "Request to ElevenLabs failed", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

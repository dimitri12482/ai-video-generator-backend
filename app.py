from flask import Flask, request, send_file, jsonify
import requests
import tempfile
import os

app = Flask(__name__)

# 🔐 Secure: Set this in your Render or local environment
ELEVENLABS_API_KEY = os.environ.get("sk_e68b861d8d119bd6bd0cb2451d12df46d8a99c85bfc8d669")
VOICE_ID = "b38kUX8pkfYO2kHyqfFy"  # Example voice ID (you should replace this)

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Text is required"}), 400

    # ElevenLabs API call with WAV format
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

    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream?output_format=pcm_44100"
    response = requests.post(tts_url, headers=headers, json=payload, stream=True)

    print("Requesting ElevenLabs API for text:", text)
    print("Status code:", response.status_code)
    if response.status_code != 200:
        print("Response text:", response.text)
        return jsonify({"error": "Failed to generate audio"}), 500

    # Save audio to temporary WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                tmp_file.write(chunk)
        tmp_file_path = tmp_file.name

    return send_file(tmp_file_path, mimetype="audio/wav", as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

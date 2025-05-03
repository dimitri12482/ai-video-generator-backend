from flask import Flask, request, send_file, jsonify
import requests
import tempfile
import os

app = Flask(__name__)

# 🔐 Secure: Set this in your Render or local environment
ELEVENLABS_API_KEY = os.environ.get("sk_e68b861d8d119bd6bd0cb2451d12df46d8a99c85bfc8d669")
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Example voice ID (you should replace this)

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Text is required"}), 400

    # Log the request
    print("🔊 Speaking:", text)

    # Prepare headers and payload
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

    # Request to ElevenLabs
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    response = requests.post(url, headers=headers, json=payload, stream=True)

    # Log status and error messages if needed
    print("🔍 Status Code:", response.status_code)
    if response.status_code != 200:
        print("❌ Error:", response.text)
        return jsonify({"error": "Failed to generate audio", "details": response.text}), 500

    # Save response to temporary MP3 file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                tmp_file.write(chunk)
        tmp_file_path = tmp_file.name

    print("✅ MP3 generated at", tmp_file_path)

    # Serve the audio file
    return send_file(tmp_file_path, mimetype="audio/mpeg", as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

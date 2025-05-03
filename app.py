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
     text = data.get("text", "").strip()
     text = data.get("text", "")
 
     if not text:
         return jsonify({"error": "Text is required"}), 400
 
     if not ELEVENLABS_API_KEY:
         return jsonify({"error": "Missing ELEVENLABS_API_KEY"}), 500
 
     # Request ElevenLabs TTS
     tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
     # ElevenLabs API call with WAV format
     headers = {
         "xi-api-key": ELEVENLABS_API_KEY,
         "Content-Type": "application/json"
 @@ -38,22 +30,23 @@ def speak():
         }
     }
 
     print(f"🔄 Sending TTS request for text: {text}")
     tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream?output_format=pcm_44100"
     response = requests.post(tts_url, headers=headers, json=payload, stream=True)
 
     print("Requesting ElevenLabs API for text:", text)
     print("Status code:", response.status_code)
     if response.status_code != 200:
         print("❌ ElevenLabs error:", response.text)
         return jsonify({"error": "Failed to generate audio", "details": response.text}), 500
         print("Response text:", response.text)
         return jsonify({"error": "Failed to generate audio"}), 500
 
     # Save to temp file
     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
     # Save audio to temporary WAV file
     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
         for chunk in response.iter_content(chunk_size=1024):
             if chunk:
                 tmp_file.write(chunk)
         tmp_file_path = tmp_file.name
 
     print("✅ Audio generated and saved to:", tmp_file_path)
     return send_file(tmp_file_path, mimetype="audio/mpeg", as_attachment=False)
     return send_file(tmp_file_path, mimetype="audio/wav", as_attachment=False)
 
 if __name__ == "__main__":
     app.run(debug=True, port=5000)

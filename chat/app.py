from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder=".")

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2"  # make sure you ran: ollama pull llama3.2


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message first."})

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an AI assistant. Answer clearly and concisely."
                    },
                    {"role": "user", "content": user_message},
                ],
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        reply = data["message"]["content"]
        return jsonify({"reply": reply})
    except Exception:
        # Most common case: Ollama server is not running / not reachable
        return jsonify({"reply": "Ollama server is not running. Please start it."})


if __name__ == "__main__":
    app.run(debug=True)

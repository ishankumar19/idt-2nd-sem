from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import json
import urllib.request

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json or {}

    weak_topics   = data.get("weak_topics", [])
    strong_topics = data.get("strong_topics", [])
    q_count       = int(data.get("q_count", 10))
    pdf_base64    = data.get("pdf_base64", None)
    api_key       = data.get("api_key") or GEMINI_API_KEY

    if not api_key or api_key.strip() == "":
        return jsonify({"error": "Please provide a valid Google Gemini API key"}), 400

    weak_count   = round(q_count * 0.65)
    strong_count = q_count - weak_count

    prompt = f"""You are an adaptive quiz generator. Generate exactly {q_count} MCQ questions in JSON format.

Topics distribution:
- Weak areas (generate {weak_count} questions): {', '.join(weak_topics) if weak_topics else 'general topics'}
- Strong areas (generate {strong_count} questions): {', '.join(strong_topics) if strong_topics else 'same topics but easier'}

Rules:
- Weak topic questions: moderately challenging
- Strong topic questions: straightforward
- Each question must have exactly 4 options (A, B, C, D)
- Provide correct answer index (0-3) and a brief explanation

Respond ONLY with a valid JSON array, no markdown, no extra text."""

    parts = []
    if pdf_base64:
        parts.append({
            "inline_data": {
                "mime_type": "application/pdf",
                "data": pdf_base64
            }
        })
    parts.append({"text": prompt})

    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 8192,
            "responseMimeType": "application/json"
        }
    }

    model = "gemini-3-flash-preview"
    url   = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        return jsonify({"error": f"Gemini API error {e.code}: {err_body}"}), 502
    except Exception as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500

    try:
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        text = text.replace("```json", "").replace("```", "").strip()
        questions = json.loads(text)

        if questions:
            print("=== GEMINI QUESTION SAMPLE ===")
            print(json.dumps(questions[0], indent=2))
            print("==============================")

        return jsonify({"questions": questions})

    except Exception as e:
        return jsonify({
            "error": "Failed to parse Gemini response",
            "details": str(e)
        }), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

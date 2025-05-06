from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

HUGGINGFACE_TOKEN = os.getenv("HF_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
    "Content-Type": "application/json"
}

MODELS = {
    "sentiment": "HooshvareLab/bert-fa-sentiment-digikala",
    "topic": "HooshvareLab/persian-news-category-classifier",
    "summary": "MBZUAI/LaMini-Flan-T5-248M"
}

def query_huggingface(model, payload):
    url = f"https://api-inference.huggingface.co/models/{model}"
    response = requests.post(url, headers=HEADERS, json=payload)
    try:
        return response.json()
    except:
        return {"error": "Invalid JSON response"}

@app.route("/analyze", methods=["POST"])
def analyze_text():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    input_text = data["text"]
    results = {
        "sentiment": query_huggingface(MODELS["sentiment"], {"inputs": input_text}),
        "topic": query_huggingface(MODELS["topic"], {"inputs": input_text}),
        "summary": query_huggingface(MODELS["summary"], {"inputs": input_text})
    }
    return jsonify(results)

# Local dev endpoint to simulate form field combination
@app.route("/simulate_entry", methods=["POST"])
def simulate_entry():
    entry = request.get_json()
    text_parts = []
text_parts.append(rgar(entry, '21'))  # فیلد 21
text_parts.append(rgar(entry, '33'))  # فیلد 33
text_parts.append(rgar(entry, '36'))  # فیلد 36
text_parts.append(rgar(entry, '44'))  # فیلد 44
text_parts.append(rgar(entry, '49'))  # فیلد 49
text_parts.append(rgar(entry, '57'))  # فیلد 57
text_parts.append(rgar(entry, '59'))  # فیلد 59
text_parts.append(rgar(entry, '64'))  # فیلد 64
text_parts.append(rgar(entry, '71'))  # فیلد 71
text_parts.append(rgar(entry, '78'))  # فیلد 78
text_parts.append(rgar(entry, '79'))  # فیلد 79
text_parts.append(rgar(entry, '121'))  # فیلد 121
text_parts.append(rgar(entry, '140'))  # فیلد 140
text_parts.append(rgar(entry, '142'))  # فیلد 142
text_parts.append(rgar(entry, '152'))  # فیلد 152
    text = '\n'.join([part for part in text_parts if part])
    return analyze_text()

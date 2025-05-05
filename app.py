import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

HF_TOKEN = os.environ.get("HF_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# مدل‌ها
SENTIMENT_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"
TOPIC_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

CATEGORIES = [
    "Fintech", "HealthTech", "EdTech", "AgriTech", "FoodTech",
    "E-Commerce", "TransportTech", "InsurTech", "Cybersecurity", "BioTech"
]

@app.route("/", methods=["GET"])
def home():
    return "Bamasaz AI middleware is active."

@app.route("/proxy", methods=["POST"])
def proxy():
    try:
        input_data = request.json
        text = input_data.get("text", "").strip()

        if not text:
            return jsonify({"error": "متن خالی است."}), 400

        # تحلیل احساس
        sent_payload = {"inputs": text}
        sent_response = requests.post(SENTIMENT_URL, headers=HEADERS, json=sent_payload)
        sentiment = sent_response.json()

        # تحلیل موضوع
        topic_payload = {
            "inputs": text,
            "parameters": {"candidate_labels": CATEGORIES}
        }
        topic_response = requests.post(TOPIC_URL, headers=HEADERS, json=topic_payload)
        topic = topic_response.json()

        return jsonify({
            "sentiment": sentiment,
            "topic": topic
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

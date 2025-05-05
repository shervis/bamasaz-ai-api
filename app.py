import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

HF_TOKEN = os.environ.get("HF_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# مسیر مدل‌های HuggingFace
SENTIMENT_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
TOPIC_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

# برچسب‌های موضوعی
CATEGORIES = [
    "Fintech", "HealthTech", "EdTech", "AgriTech", "FoodTech",
    "E-Commerce", "TransportTech", "InsurTech", "Cybersecurity", "BioTech"
]

@app.route("/", methods=["GET"])
def home():
    return "Bamasaz AI middleware is active with sentiment & topic classification."

@app.route("/proxy", methods=["POST"])
def proxy():
    try:
        input_data = request.json
        text = input_data.get("text", "").strip()

        if not text:
            return jsonify({"error": "متن ورودی خالی است"}), 400

        # تحلیل احساس
        sentiment_payload = {"inputs": text}
        sentiment_response = requests.post(SENTIMENT_URL, headers=HEADERS, json=sentiment_payload)
        if sentiment_response.status_code != 200:
            return jsonify({"error": f"خطا در مدل احساس: {sentiment_response.status_code}"}), 500
        sentiment_result = sentiment_response.json()

        # تحلیل موضوع
        topic_payload = {
            "inputs": text,
            "parameters": {"candidate_labels": CATEGORIES}
        }
        topic_response = requests.post(TOPIC_URL, headers=HEADERS, json=topic_payload)
        if topic_response.status_code != 200:
            return jsonify({"error": f"خطا در مدل موضوع: {topic_response.status_code}"}), 500
        topic_result = topic_response.json()

        # ترکیب نتایج
        result = {
            "sequence": text,
            "sentiment": sentiment_result,
            "topic": {
                "labels": topic_result.get("labels", []),
                "scores": topic_result.get("scores", [])
            }
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

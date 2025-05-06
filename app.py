
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

HF_TOKEN = os.environ.get("HF_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

SENTIMENT_URL = "https://api-inference.huggingface.co/models/HooshvareLab/bert-fa-base-uncased-sentiment-digikala"
TOPIC_URL = "https://api-inference.huggingface.co/models/HooshvareLab/bert-fa-base-uncased-clf-persiannews"

@app.route("/", methods=["GET"])
def home():
    return "Bamasaz AI middleware is active."

@app.route("/proxy", methods=["POST"])
def proxy():
    try:
        input_data = request.json
        text_parts = [
            input_data.get("21", ""),
            input_data.get("33", ""),
            input_data.get("36", ""),
            input_data.get("44", ""),
            input_data.get("49", ""),
            input_data.get("57", ""),
            input_data.get("59", ""),
            input_data.get("64", ""),
            input_data.get("71", ""),
            input_data.get("78", ""),
            input_data.get("79", ""),
            input_data.get("121", ""),
            input_data.get("140", ""),
            input_data.get("142", ""),
            input_data.get("152", "")
        ]
        text = '\n'.join([part for part in text_parts if part])

        # تحلیل احساس
        sentiment_response = requests.post(SENTIMENT_URL, headers=HEADERS, json={"inputs": text})
        sentiment_result = sentiment_response.json()

        # تحلیل موضوع
        topic_response = requests.post(TOPIC_URL, headers=HEADERS, json={"inputs": text})
        topic_result = topic_response.json()

        # ساخت خروجی ترکیبی
        output = {
            "sentiment": sentiment_result,
            "topic": topic_result,
            "text": text
        }
        return jsonify(output)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

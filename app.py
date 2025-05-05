
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
            return jsonify({"error": "No input text provided"}), 400

        payload = {"inputs": text}
        response = requests.post(SENTIMENT_URL, headers=HEADERS, json=payload)
        result = response.json()

        return jsonify({"sentiment": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/classify", methods=["POST"])
def classify():
    try:
        input_data = request.json
        text = input_data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No input text provided"}), 400

        payload = {
            "inputs": text,
            "parameters": {"candidate_labels": CATEGORIES}
        }

        response = requests.post(TOPIC_URL, headers=HEADERS, json=payload)
        result = response.json()

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

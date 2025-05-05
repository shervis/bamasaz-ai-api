import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

HF_TOKEN = os.environ.get("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

CATEGORIES = [
    "Fintech", "HealthTech", "EdTech", "AgriTech", "PropTech",
    "FoodTech", "E-Commerce", "TransportTech", "GreenTech", "InsurTech",
    "SaaS", "Data Science", "Cybersecurity", "Entertainment", "BioTech",
    "HRTech", "LegalTech", "GovTech", "RegTech", "Advertising"
]

@app.route("/classify", methods=["POST"])
def classify():
    input_data = request.json
    text = input_data.get("text", "").strip()

    if not text:
        return jsonify({"error": "متن ورودی خالی است"}), 400

    payload = {
        "inputs": text,
        "parameters": {"candidate_labels": CATEGORIES}
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return jsonify({"error": "خطا در اتصال به مدل", "detail": response.json()}), response.status_code

    result = response.json()
    return jsonify({"result": result})

@app.route("/", methods=["GET"])
def home():
    return "Bamasaz AI classification API is live."

if __name__ == "__main__":
    app.run(debug=True)

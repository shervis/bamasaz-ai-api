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

candidate_labels = [
    "Fintech", "HealthTech", "EdTech", "AgriTech", "FoodTech",
    "E-Commerce", "TransportTech", "InsurTech", "Cybersecurity", "BioTech"
]

@app.route("/", methods=["GET"])
def home():
    return "Bamasaz AI classification service is live!"

@app.route("/classify", methods=["POST"])
def classify():
    input_data = request.json
    text = input_data.get("text", "")

    if not text:
        return jsonify({"error": "متن ورودی خالی است"}), 400

    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": candidate_labels
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return jsonify({"error": "خطا در اتصال به مدل", "detail": response.json()}), response.status_code

    result = response.json()
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)

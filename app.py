import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

HF_TOKEN = os.environ.get("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

@app.route("/analyze", methods=["POST"])
def analyze():
    input_data = request.json
    text = input_data.get("text", "")

    if not text:
        return jsonify({"error": "متن ورودی خالی است"}), 400

    response = requests.post(API_URL, headers=headers, json={"inputs": text})

    if response.status_code != 200:
        return jsonify({"error": "خطا در اتصال یا احراز هویت", "detail": response.json()}), response.status_code

    result = response.json()
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)

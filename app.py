import os
import requests
import traceback
from flask import Flask, request, jsonify

app = Flask(__name__)

# دریافت توکن از محیط
HF_TOKEN = os.environ.get("HF_TOKEN")

# هدر برای Hugging Face API
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# URL مدل‌های Hugging Face
SENTIMENT_URL = "https://api-inference.huggingface.co/models/HooshvareLab/bert-fa-base-uncased-sentiment-snappfood"
TOPIC_URL = "https://api-inference.huggingface.co/models/HooshvareLab/bert-fa-base-uncased-clf-persiannews"

@app.route("/", methods=["GET"])
def home():
    return "✅ Bamasaz AI middleware is active."

@app.route("/proxy", methods=["POST"])
def proxy():
    try:
        # لاگ اولیه برای ورودی
        print("🎯 Raw input received:", request.get_data(as_text=True))

        input_data = request.json

        if not HF_TOKEN:
            print("🚫 HF_TOKEN is missing from environment variables.")
            return jsonify({"error": "HF_TOKEN is missing"}), 403

        # استخراج فیلدهای متنی
        text_parts = [input_data.get(str(f), "") for f in [21, 33, 36, 44, 49, 57, 59, 64, 71, 78, 79, 121, 140, 142, 152]]
        text = '\n'.join([part for part in text_parts if part]).strip()

        if not text:
            print("⚠️ No text content found for analysis.")
            return jsonify({"error": "هیچ متنی برای تحلیل ارسال نشده است."}), 400

        # ارسال به مدل تحلیل احساس
        sentiment_response = requests.post(SENTIMENT_URL, headers=HEADERS, json={"inputs": text})
        print("📦 Sentiment response:", sentiment_response.text)
        sentiment_result = sentiment_response.json()

        if sentiment_response.status_code != 200 or "error" in sentiment_result:
            return jsonify({
                "error": "❌ خطا در مدل تحلیل احساس",
                "details": sentiment_result.get("error", "نامشخص")
            }), 503

        # ارسال به مدل تحلیل موضوع
        topic_response = requests.post(TOPIC_URL, headers=HEADERS, json={"inputs": text})
        print("📦 Topic response:", topic_response.text)
        topic_result = topic_response.json()

        if topic_response.status_code != 200 or "error" in topic_result:
            return jsonify({
                "error": "❌ خطا در مدل تحلیل موضوع",
                "details": topic_result.get("error", "نامشخص")
            }), 503

        # خروجی نهایی
        output = {
            "sentiment": sentiment_result,
            "topic": topic_result,
            "text": text
        }

        return jsonify(output)

    except Exception as e:
        print("🔥 Unexpected error:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

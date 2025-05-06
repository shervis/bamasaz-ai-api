import os
import requests
import traceback
from flask import Flask, request, jsonify

app = Flask(__name__)

# گرفتن توکن Hugging Face از متغیر محیطی
HF_TOKEN = os.environ.get("HF_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# ✅ مدل‌های Hugging Face آماده و در دسترس
SENTIMENT_URL = "https://api-inference.huggingface.co/models/HooshvareLab/bert-fa-base-uncased-sentiment-digikala"
TOPIC_URL = "https://api-inference.huggingface.co/models/HooshvareLab/bert-fa-base-uncased-clf-persiannews"

@app.route("/", methods=["GET"])
def home():
    return "✅ Bamasaz AI middleware is active."

@app.route("/proxy", methods=["POST"])
def proxy():
    try:
        # لاگ ورودی
        print("🎯 Raw input received:", request.get_data(as_text=True))
        input_data = request.json

        if not HF_TOKEN:
            print("🚫 HF_TOKEN is missing.")
            return jsonify({"error": "HF_TOKEN is missing"}), 403

        # ترکیب فیلدهای متنی
        text_parts = [input_data.get(str(f), "") for f in [21, 33, 36, 44, 49, 57, 59, 64, 71, 78, 79, 121, 140, 142, 152]]
        text = '\n'.join([part for part in text_parts if part]).strip()

        if not text:
            return jsonify({"error": "هیچ متنی برای تحلیل ارسال نشده است."}), 400

        # تحلیل احساس
        sentiment_response = requests.post(SENTIMENT_URL, headers=HEADERS, json={"inputs": text})
        print("📦 Sentiment raw response:", sentiment_response.text)
        print("📦 Sentiment status code:", sentiment_response.status_code)

        try:
            sentiment_result = sentiment_response.json()
        except Exception:
            return jsonify({
                "error": "پاسخ نامعتبر از مدل تحلیل احساس",
                "raw": sentiment_response.text
            }), 500

        if sentiment_response.status_code != 200 or "error" in sentiment_result:
            return jsonify({
                "error": "❌ خطا در مدل تحلیل احساس",
                "details": sentiment_result.get("error", "نامشخص")
            }), 503

        # تحلیل موضوع
        topic_response = requests.post(TOPIC_URL, headers=HEADERS, json={"inputs": text})
        print("📦 Topic raw response:", topic_response.text)
        print("📦 Topic status code:", topic_response.status_code)

        try:
            topic_result = topic_response.json()
        except Exception:
            return jsonify({
                "error": "پاسخ نامعتبر از مدل تحلیل موضوع",
                "raw": topic_response.text
            }), 500

        if topic_response.status_code != 200 or "error" in topic_result:
            return jsonify({
                "error": "❌ خطا در مدل تحلیل موضوع",
                "details": topic_result.get("error", "نامشخص")
            }), 503

        # پاسخ نهایی
        return jsonify({
            "sentiment": sentiment_result,
            "topic": topic_result,
            "text": text
        })

    except Exception as e:
        print("🔥 Unexpected error:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# مدل احساس
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# مدل تحلیل موضوعی (zero-shot)
topic_pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# دسته‌بندی‌های پیشنهادی (می‌توان ویرایش کرد)
candidate_labels = [
    "Fintech", "HealthTech", "EdTech", "AgriTech", "PropTech",
    "GreenTech", "E-commerce", "FoodTech", "Entertainment", "AI & Analytics"
]

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text.strip():
            return jsonify({"error": "Empty text provided"}), 400

        # تحلیل احساس
        sentiment_result = sentiment_pipeline(text)

        # تحلیل موضوعی
        topic_result = topic_pipeline(text, candidate_labels)
        top_topic = topic_result["labels"][0]

        return jsonify({
            "result": sentiment_result,
            "topic": top_topic
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

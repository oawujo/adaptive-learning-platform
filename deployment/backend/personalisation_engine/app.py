
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    score = int(data.get("score", 0))
    time_spent = int(data.get("time_spent", 0))
    content_type = data.get("content_type", "text")

    if score < 50:
        recommendation = "Review the basics with a simpler video lesson."
    elif score < 75:
        recommendation = "Try a quiz to reinforce this concept."
    elif content_type == "text":
        recommendation = "Watch a short video to deepen your understanding."
    else:
        recommendation = "Advance to the next topic with an interactive exercise."

    return jsonify({"recommendation": recommendation})

@app.route("/", methods=["GET"])
def index():
    return {"message": "Personalisation Engine is running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8002))
    app.run(host="0.0.0.0", port=port)

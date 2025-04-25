#
# from flask import Flask, request, jsonify
# import os
#
# app = Flask(__name__)
#
# @app.route("/recommend", methods=["POST"])
# def recommend():
#     data = request.get_json()
#     score = int(data.get("score", 0))
#     time_spent = int(data.get("time_spent", 0))
#     content_type = data.get("content_type", "text")
#
#     if score < 50:
#         recommendation = "Review the basics with a simpler video lesson."
#     elif score < 75:
#         recommendation = "Try a quiz to reinforce this concept."
#     elif content_type == "text":
#         recommendation = "Watch a short video to deepen your understanding."
#     else:
#         recommendation = "Advance to the next topic with an interactive exercise."
#
#     return jsonify({"recommendation": recommendation})
#
# @app.route("/", methods=["GET"])
# def index():
#     return {"message": "Personalisation Engine is running"}
#
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8002))
#     app.run(host="0.0.0.0", port=port)
#
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# Dummy function to simulate learner history retrieval
def load_logs(user_id):
    # For this demo, we use a simple local JSON file or placeholder
    logs_path = f"./logs/{user_id}.json"
    if not os.path.exists(logs_path):
        return []
    with open(logs_path, "r") as f:
        return json.load(f)

# Dummy logic for recommendation
def recommend_next(logs):
    if not logs:
        return None

    last_topic = logs[-1].get("topic", "Introduction to AI")
    topic_map = {
        "Photosynthesis": ("Cellular Respiration", "intermediate"),
        "Machine Learning": ("Neural Networks", "intermediate"),
        "Neural Networks": ("Deep Learning", "advanced"),
        "Introduction to AI": ("Machine Learning", "beginner"),
    }
    return topic_map.get(last_topic, ("General Review", "beginner"))

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json()
        user_id = data.get("user_id")

        if not user_id:
            return jsonify({"error": "Missing user_id"}), 400

        logs = load_logs(user_id)

        if not logs:
            return jsonify({"message": "No logs found", "topic": "Introduction to AI", "level": "beginner"}), 200

        topic, level = recommend_next(logs)
        return jsonify({"topic": topic, "level": level})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def health():
    return "Personalisation Engine is running", 200
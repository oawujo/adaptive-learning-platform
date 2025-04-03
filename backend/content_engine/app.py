
from flask import Flask, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/generate", methods=["POST"])
def generate_content():
    data = request.get_json()
    topic = data.get("topic", "AI Fundamentals")
    level = data.get("level", "beginner")
    style = data.get("style", "text")

    prompt = f"""
    Generate a {style} learning module for the topic: "{topic}".
    Make it suitable for a {level} level student.
    Include a summary, 2 examples, and 2 quiz questions at the end.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful AI tutor that creates personalized lessons."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"generated_content": content})

@app.route("/", methods=["GET"])
def index():
    return {"message": "Content Engine (GPT-4o powered) is running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8003))
    app.run(host="0.0.0.0", port=port)

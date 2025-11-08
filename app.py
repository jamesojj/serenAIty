from flask import Flask, render_template
from dotenv import load_dotenv
import openai
import os

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("REDACTED")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are SerenAIty, a calm, supportive wellness companion "
                "who helps students manage stress, mood, self-awareness, and "
                "emotional balance. You speak gently, in short, warm sentences."
            )},

            {"role": "user", "content": user_message}
        ]
    )

    ai_message = response["choices"][0]["message"]["content"]

    return jsonify({"reply: ai_message"})

if __name__ == "__main__":
    app.run(debug=True)
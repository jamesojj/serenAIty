from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
from datetime import datetime

load_dotenv()

app = Flask(__name__)

client = OpenAI()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    
    user_message = request.json["message"]

    mood_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Respond with only one word: calm, happy, neutral, tired, stressed, anxious, overwhelmed."},
            {"role": "user", "content": user_message}
        ]
    )
    detected_mood = mood_response.choices[0].message.content.lower()

    with open("data/mood_log.json", "r") as f:
        mood_log = json.load(f)

    mood_log.append({"mood": detected_mood, "timestamp": datetime.now().isoformat()})

    with open("data/mood_log.json", "w") as f:
        json.dump(mood_log, f, indent=2)

    recent_moods = [entry["mood"] for entry in mood_log[-3:]]
    stressed_streak = recent_moods.count("stressed")

    if stressed_streak >= 2:
        return jsonify({ 
            "reply": "breathing_excercise",
            "mood": detected_mood
        })

    chat_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are SerenAIty, a calm and gentle wellness companion."},
            {"role": "user", "content": user_message}
        ]
    )

    ai_message = chat_response.choices[0].message.content
    return jsonify({"reply": ai_message, "mood": detected_mood})


if __name__ == "__main__":
    app.run(debug=True)
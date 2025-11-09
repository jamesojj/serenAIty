from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
from datetime import datetime

load_dotenv() # for secure API key access

app = Flask(__name__)

client = OpenAI() # Loads securely from .env 

@app.route("/")
def home():
    # Renders in the main chat interface UI
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Allows the users message typed to enter the chat interface
    user_message = request.json["message"]

    # KEY FEATURE: Mood Detection Agent permitting autonomous emotional reading of the user. 
    # This is done by reading the emotional tone from the user and classifying it in one word allowing SerenAIty to understand emotions and not just reply.

    mood_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Respond with only one word: calm, happy, neutral, tired, stressed, anxious, overwhelmed."},
            {"role": "user", "content": user_message}
        ]
    )

    detected_mood = mood_response.choices[0].message.content.lower()

    # Recording the mood history to recognise patterns from the user enabling the app to sense emotion trends over a duration.

    with open("data/mood_log.json", "r") as f:
        mood_log = json.load(f)

    mood_log.append({
        "mood": detected_mood, 
        "timestamp": datetime.now().isoformat()
    })

    with open("data/mood_log.json", "w") as f:
        json.dump(mood_log, f, indent=2)

    # Senses stress patterns for example if the user is displaying signs of stress in their responses consecutively, SerenAIty takes the intiative and walks the user through a grounding exercise.

    recent_moods = [entry["mood"] for entry in mood_log[-3:]]
    stressed_streak = recent_moods.count("stressed")

    if stressed_streak >= 2:
        return jsonify({ 
            "reply": "breathing_excercise",
            "mood": detected_mood
        })

    # The normal supportive chat mode of SerenAIty 

    chat_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are SerenAIty, a calm and gentle wellness companion."},
            {"role": "user", "content": user_message}
        ]
    )

    ai_message = chat_response.choices[0].message.content

    # Returning reply + mood so the frontend can display the mood tag
    return jsonify({"reply": ai_message, "mood": detected_mood})


if __name__ == "__main__":
    app.run(debug=True)
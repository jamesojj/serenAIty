from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
import random
from datetime import datetime

load_dotenv() # for secure API key access

app = Flask(__name__)

pending_followup = None

client = OpenAI() # Loads securely from .env 



@app.route("/")
def home():
    # Renders in the main chat interface UI
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Allows the users message typed to enter the chat interface
    user_message = request.json["message"]

    global pending_followup

    if pending_followup and user_message.lower() in ["yes", "sure", "ok", "okay", "yea", "yeah", "yep", "yh"]:
        place = pending_followup["place"]
        pending_followup = None

        maps_url = f"https://www.google.com/maps/search/?api=1&query={place['name'].replace(' ', '+')}+Manchester"

        return jsonify({
            "reply": (
                f"Great! <br><br>"
                f"Here are walking directions to <b>{place['name']}</b>:<br>"
                f"<a href=\"{maps_url}\" target=\"_blank\">Open in Google Maps</a><br><br>"
                f"Take your time. Walk slowly. Breathe naturally.<br>"
                f"I’ll be right here when you get back!"

            ),
            "mood": "encouraging"
        })

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

    # Keep mood log from growing too far - maintains last 10 entries only
    mood_log = mood_log[-10:]


    with open("data/mood_log.json", "w") as f:
        json.dump(mood_log, f, indent=2)

    # Senses stress patterns for example if the user is displaying signs of stress in their responses consecutively, SerenAIty takes the intiative and walks the user through a grounding exercise.

    recent_moods = [entry["mood"] for entry in mood_log[-3:]]

    # Detects if the last two or three moods from user were stress
    last_two_stressed = len(recent_moods) >= 2 and all(m == "stressed" for m in recent_moods[-2:])
    last_three_stressed = len(recent_moods) >= 3 and all(m == "stressed" for m in recent_moods[-3:])

    # Tiered agentic responding logic

    # Third level of intervention resulting in change of environment
    if last_three_stressed:
        with open("data/places.json", "r") as f:
            places = json.load(f)

        suggested = random.choice(places)

        # Allowing the Agent to read said instances
        
        pending_followup = {"type": "location", "place": suggested}

        return jsonify({
            "reply": (
                f"I've noticed you've been feeling stress for a while lately <br><br>"
                f"Sometimes a small change of environment can help reset your mind.<br><br>"
                f"{suggested['note']}<br><br>"
                f"Would you like me to get <u>walking directions</u>?"
            ),
            "mood": detected_mood
        })

    # Second level of intervention resulting in breathing exercise
    elif last_two_stressed:
        return jsonify({ 
            "reply": "breathing_exercise",
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
# SerenAIty
### *A calm, emotion-aware wellness companion for students.*

![Status](https://img.shields.io/badge/Status-Prototype-green)
![Built With](https://img.shields.io/badge/Tech-Flask%20%7C%20OpenAI%20API%20%7C%20HTML%20%7C%20CSS%20%7C%20JS-blueviolet)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## Overview
**SerenAIty** is an AI-powered companion designed to support student mental wellbeing.  
It doesn't only respond — it *notices* emotional patterns. When stress appears repeatedly, SerenAIty **intervenes gently** with:
- Grounding breathing exercises
- Supportive conversation
- Suggestions for calming nearby environments

This moves beyond a chatbot.  
It becomes **a companion that cares**.

---

## Key Features
| Feature | Description |
|--------|-------------|
| **Emotion Detection** | Detects emotional tone in each message |
| **Stress Pattern Tracking** | Observes changes in mood over time |
| **Guided Breathing Support** | Offered automatically when stress builds |
| **Environment Reset Suggestions** | Recommends a calming nearby space when stress persists |
| **Gentle Conversational Tone** | Designed to feel supportive, not clinical |

---

## How It Works
SerenAIty follows a **tiered emotional support flow**:

1. **Normal Chat Mode**  
   Supportive conversation when mood is stable.

2. **Breathing Intervention** *(if stress appears twice in a row)*  
   → Calm breathing guidance displayed in the chat.

3. **Environment Reset Suggestion** *(if stress persists further)*  
   → Recommends a nearby calming place (e.g., HOME Manchester).

This helps users **pause → breathe → reset**.

---

## Tech Stack
| Layer | Tools |
|------|-------|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python (Flask) |
| **AI Model** | OpenAI `gpt-4o-mini` |
| **State Tracking** | Lightweight `mood_log.json` |

---

## ⚙️ Setup & Usage

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd serenAIty
```
### 2. Create a virtual env & install dependencies
```
pip install -r requirements.txt
```
### 3. Add your API key to .env
```
OPENAI_API_KEY=your_key_here
```
### 4. Run the app
```
python app.py
```
### 5 Open in browser
```
http://127.0.0.1:5000
```

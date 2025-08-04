from transformers import pipeline
import json
from datetime import datetime
import random

# Load sentiment analysis pipeline once
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_mood(text):
    result = sentiment_pipeline(text)[0]
    label = result['label']
    score = result['score']
    # Map HuggingFace output to our mood and polarity
    if label == 'POSITIVE':
        mood = "Positive"
        polarity = score
    elif label == 'NEGATIVE':
        mood = "Negative"
        polarity = -score
    else:
        mood = "Neutral"
        polarity = 0.0
    # Optionally, treat low-confidence as Neutral
    if score < 0.7:
        mood = "Neutral"
        polarity = 0.0
    return mood, polarity

def get_spring_tip(mood):
    tips = {
        "Positive": [
            "Keep that sunshine energy! Go outside and enjoy the breeze 🌿",
            "Celebrate your mood with a walk among flowers 🌷",
            "Share your joy with someone today!"
        ],
        "Negative": [
            "It’s okay to feel down. Try deep breathing outdoors 🍃",
            "Spring brings change — take a moment to reset 🌱",
            "Drink water, listen to birds, and be kind to yourself 🐦"
        ],
        "Neutral": [
            "Find joy in small things today — maybe a flower or a breeze 🌼",
            "Balance is beautiful. Journal your thoughts.",
            "Try mindful tea time under the sun ☀️"
        ]
    }
    return random.choice(tips[mood])

def suggest_activity(mood, energy, social):
    # Simple rules for demo; can be expanded
    if mood == "Positive" and energy == "High":
        if social == "Social":
            return "Organize a picnic with friends in a park! 🍉🌳"
        else:
            return "Go for a nature walk and take photos of flowers! 🌷📸"
    elif mood == "Negative":
        if energy == "Low":
            return "Try gentle yoga or mindful breathing by an open window. 🧘‍♂️🌱"
        else:
            return "Take a stroll and listen to the birds. 🐦"
    elif mood == "Neutral":
        if social == "Social":
            return "Invite a friend for tea outdoors. 🍵🌼"
        else:
            return "Read a book under a tree or start a spring journal. 📖🌳"
    else:
        return "Open your window, breathe in spring air, and notice something beautiful! 🌸"

def recommend_web_activity(mood, energy, social):
    # Demo: recommend a web activity (YouTube, virtual garden, etc.)
    if mood == "Positive" and energy == "High":
        return ("Join a live virtual garden tour", "https://www.youtube.com/results?search_query=virtual+garden+tour")
    elif mood == "Negative":
        return ("Try a guided meditation for spring renewal", "https://www.youtube.com/results?search_query=spring+guided+meditation")
    elif energy == "Low":
        return ("Watch relaxing spring scenery", "https://www.youtube.com/results?search_query=spring+relaxing+scenery")
    elif social == "Social":
        return ("Join a spring-themed online event", "https://www.eventbrite.com/d/online/spring/")
    else:
        return ("Explore a virtual flower garden", "https://artsandculture.google.com/project/flowers")

def save_log(entry, mood, polarity):
    log = {
        "entry": entry,
        "mood": mood,
        "polarity": polarity,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open("spring_mood_companion/mood_log.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(log)

    with open("spring_mood_companion/mood_log.json", "w") as f:
        json.dump(data, f, indent=2)

def get_log():
    try:
        with open("spring_mood_companion/mood_log.json", "r") as f:
            return json.load(f)
    except Exception:
        return []

def random_spring_quote():
    quotes = [
        "Spring: a lovely reminder of how beautiful change can truly be.",
        "Where flowers bloom, so does hope. – Lady Bird Johnson",
        "No matter how long the winter, spring is sure to follow.",
        "The earth laughs in flowers. – Ralph Waldo Emerson",
        "Spring adds new life and new beauty to all that is. – Jessica Harrelson",
        "Blossom by blossom the spring begins. – Algernon Charles Swinburne",
        "Every spring is the only spring, a perpetual astonishment. – Ellis Peters",
        "If we had no winter, the spring would not be so pleasant. – Anne Bradstreet"
    ]
    return random.choice(quotes)

def random_activity():
    activities = [
        "Paint or draw a spring scene! 🎨",
        "Try a new herbal tea and sip it outside. 🍵",
        "Make a flower crown from wildflowers. 🌼",
        "Write a poem about spring. ✍️",
        "Plant a seed and watch it grow. 🌱",
        "Go cloud-watching and spot shapes. ☁️",
        "Listen to a spring playlist and dance! 🎶",
        "Press flowers in a book. 📖🌸",
        "Make a gratitude list inspired by nature. 🌳"
    ]
    return random.choice(activities)
import tkinter as tk
from tkinter import scrolledtext
import random
import spacy
from transformers import pipeline
from datetime import datetime

nlp = spacy.load("en_core_web_sm")
sentiment_analyzer = pipeline('sentiment-analysis')

rules = {
    "greeting": ["Hello! How can I help you today?", "Hi there! What can I do for you?", "Hey! Need any assistance?"],
    "how_are_you": ["I'm just a bot, but I'm here to help you!", "I'm an AI, so I don't have feelings, but thanks for asking!", "I'm here to assist you with anything you need!"],
    "name_query": ["I'm a simple chatbot created to assist you.", "You can call me Chatbot.", "I'm your friendly virtual assistant."],
    "goodbye": ["Goodbye! Have a great day!", "See you later!", "Take care!"],
    "capabilities": ["I can chat with you and help with basic queries!", "I'm here to provide information and assist with simple tasks.", "I can answer your questions and keep you company!"],
    "age_query": ["I'm timeless, as I exist in the digital realm!", "Age is just a number for a bot like me.", "I was created recently, but I can learn new things every day!"],
    "joke": ["Why did the scarecrow win an award? Because he was outstanding in his field!", "Why don't scientists trust atoms? Because they make up everything!", "Why did the math book look sad? Because it had too many problems."],
    "weather_query": ["I'm not equipped to provide weather updates, but you can check online!", "Weather information is not my strong suit. Try a weather app!", "I recommend using a weather service for that information."],
    "sentiment": ["It sounds like you're feeling good!", "I'm here to help if you're feeling down.", "Stay positive! Everything will be okay."],
    "small_talk": ["It's a nice day, isn't it?", "I love chatting with you!", "What else would you like to know?"],
    "favorite_color": ["I like blue, it reminds me of the sky!", "Green is nice, it's the color of nature!", "I don't have a favorite color, but I think all colors are beautiful!"],
    "time_query": ["The current time is: "],  
    "default": ["I'm sorry, I don't understand that. Can you rephrase?", "I didn't get that. Could you say it differently?", "Sorry, can you try asking in another way?"],
}

def classify_intent(user_input):
    doc = nlp(user_input)
    if any(token.lemma_ in ["hi", "hello", "hey"] for token in doc):
        return "greeting"
    elif "old" in [token.lemma_ for token in doc] and "you" in [token.lemma_ for token in doc]:
        return "age_query"
    elif "how" in [token.lemma_ for token in doc] and "you" in [token.lemma_ for token in doc]:
        return "how_are_you"
    elif "name" in [token.lemma_ for token in doc] and "your" in [token.lemma_ for token in doc]:
        return "name_query"
    elif "bye" in [token.lemma_ for token in doc] or "goodbye" in [token.lemma_ for token in doc]:
        return "goodbye"
    elif any(token.lemma_ in ["can", "what"] and "do" in [token.lemma_ for token in doc] for token in doc):
        return "capabilities"
    elif "joke" in [token.lemma_ for token in doc]:
        return "joke"
    elif "weather" in [token.lemma_ for token in doc]:
        return "weather_query"
    elif "time" in [token.lemma_ for token in doc]:
        return "time_query"
    elif "color" in [token.lemma_ for token in doc] and "favorite" in [token.lemma_ for token in doc]:
        return "favorite_color"
    elif sentiment_analyzer(user_input)[0]['label'] == 'NEGATIVE':
        return "sentiment"
    elif any(token.lemma_ in ["chat", "talk", "converse"] for token in doc):
        return "small_talk"
    else:
        return "default"

def get_response(user_input):
    intent = classify_intent(user_input)
    if intent == "time_query":
        current_time = datetime.now().strftime("%H:%M:%S")
        return f"The current time is: {current_time}"
    return random.choice(rules.get(intent, rules["default"]))

def send_message():
    user_input = user_entry.get()
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "You: " + user_input + "\n")
    user_entry.delete(0, tk.END)
    if classify_intent(user_input) == "goodbye":
        response = get_response("goodbye")
        chat_display.insert(tk.END, "Bot: " + response + "\n")
        chat_display.config(state=tk.DISABLED)
        root.after(1000, root.destroy)  
    else:
        response = get_response(user_input)
        chat_display.insert(tk.END, "Bot: " + response + "\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

def on_enter(event):
    send_message()

root = tk.Tk()
root.title("Chatbot")
root.geometry("400x500")

chat_display = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD)
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

user_entry = tk.Entry(root, font=("Arial", 14))
user_entry.pack(padx=10, pady=10, fill=tk.X)
user_entry.bind("<Return>", on_enter)

send_button = tk.Button(root, text="Send", command=send_message, font=("Arial", 14))
send_button.pack(pady=5)

root.mainloop()

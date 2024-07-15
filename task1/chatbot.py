import tkinter as tk
from tkinter import scrolledtext
import random

rules = {
    "hi": ["Hello! How can I help you today?", "Hi there! What can I do for you?", "Hey! Need any assistance?"],
    "hello": ["Hi there! How can I assist you?", "Hello! How's it going?", "Greetings! How can I help you?"],
    "how are you": ["I'm just a bot, but I'm here to help you!", "I'm an AI, so I don't have feelings, but thanks for asking!", "I'm here to assist you with anything you need!"],
    "what's your name": ["I'm a simple chatbot created to assist you.", "You can call me Chatbot.", "I'm your friendly virtual assistant."],
    "what can you do": ["I can chat with you and help with basic queries!", "I'm here to provide information and assist with simple tasks.", "I can answer your questions and keep you company!"],
    "how old are you": ["I'm timeless, as I exist in the digital realm!", "Age is just a number for a bot like me.", "I was created recently, but I can learn new things every day!"],
    "tell me a joke": ["Why did the scarecrow win an award? Because he was outstanding in his field!", "Why don't scientists trust atoms? Because they make up everything!", "Why did the math book look sad? Because it had too many problems."],
    "what's the weather": ["I'm not equipped to provide weather updates, but you can check online!", "Weather information is not my strong suit. Try a weather app!", "I recommend using a weather service for that information."],
    "default": ["I'm sorry, I don't understand that. Can you rephrase?", "I didn't get that. Could you say it differently?", "Sorry, can you try asking in another way?"],
    "bye": ["Goodbye! Have a great day!", "See you later!", "Take care!"],
}

def get_response(user_input):
    user_input = user_input.lower()
    return random.choice(rules.get(user_input, rules["default"]))

def send_message():
    user_input = user_entry.get()
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "You: " + user_input + "\n")
    user_entry.delete(0, tk.END)
    if user_input.lower() == "bye":
        response = get_response("bye")
        chat_display.insert(tk.END, "Bot: " + response + "\n")
        chat_display.config(state=tk.DISABLED)
        root.after(2000, root.destroy)  # Close the window after 2 seconds
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

#dictionary of rules
rules = {
    "hi": "Hello! How can I help you today?",
    "hello": "Hi there! How can I assist you?",
    "how are you": "I'm just a bot, but I'm here to help you!",
    "what's your name": "I'm a simple chatbot created to assist you.",
    "bye": "Goodbye! Have a great day!",
    "default": "I'm sorry, I don't understand that. Can you rephrase?"
}

def get_response(user_input):
    user_input = user_input.lower()  
    return rules.get(user_input, rules["default"]) 

def chatbot():
    print("Welcome to the chatbot! Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("Bot: " + get_response("bye"))
            break
        else:
            response = get_response(user_input)
            print("Bot: " + response)

chatbot()
import random

import streamlit as st

# Set the title of the app
st.title("Welcome to My First Streamlit App")

# Add a text input
name = st.text_input("Enter your name:")

# Display the name entered by the user
if name:
    st.write(f"Hello, {name}! Welcome to the app.")
get_chatbot_response = {
    "hi": [
         "Hello! I am Chatty, here to assist you in finding medical services within St. Kitts?"
    ],
    "i have some questions dealing with my mental health": [
            "Sure, ask away!"
    ],
    
}
while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "bye":
        print("Alex: Ok bye")
        break # exit the loop when the user types 'bye'
    elif user_input.lower() in get_chatbot_response: 
        # Access dictionary values using square brackets and the key
        print("Alex:", random.choice(get_chatbot_response[user_input.lower()]))

import streamlit as st
from transformers import pipeline

# Load the pre-trained text generation model
generator = pipeline("text-generation", model="gpt2")

# Streamlit app layout
st.title("Chatty: Your Conversational AI")
st.write("Hello! I am Chatty, your conversational AI. Type something to start a conversation:")

# Input box for user message
user_input = st.text_input("You:")

# If user input is provided
if user_input:
    # Generate a response from the AI
    response = generator(user_input, max_length=50, num_return_sequences=1)
    ai_response = response[0]['generated_text']
    
    # Display the AI's response
    st.write("Chatty:", ai_response)



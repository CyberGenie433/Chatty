import streamlit as st
import openai

# Set up your OpenAI API key
openai.api_key = "your_openai_api_key_here"

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

# Streamlit app layout
st.title("Chatty: Your Conversational AI")
st.write("Hello! I am Chatty, your conversational AI. How can I assist you today?")

# Input box for user message
user_input = st.text_input("You:")

# If user input is provided
if user_input:
    # Generate a response from the AI
    ai_response = generate_response(user_input)
    
    # Display the AI's response
    st.write("Chatty:", ai_response)



import streamlit as st
import openai
import os

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure to set this in your environment variables

def get_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use appropriate engine
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI
st.title("Mental Health Chatbot")

user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        prompt = f"You are a mental health support chatbot. Respond empathetically and supportively to the following message: {user_input}"
        response = get_response(prompt)
        st.text_area("Bot:", response, height=150)
    else:
        st.warning("Please enter a message before pressing Send.")

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
st.title("Chatty - Mental Health Chatbot")

# Define a state to store the chat history
if 'history' not in st.session_state:
    st.session_state.history = []

def submit_message():
    if st.session_state.user_input:
        prompt = f"You are Chatty, a mental health support chatbot. Respond empathetically and supportively to the following message: {st.session_state.user_input}"
        response = get_response(prompt)
        st.session_state.history.append({"user": st.session_state.user_input, "bot": response})
        st.session_state.user_input = ""  # Clear input field after submission

# Text area for user input
st.text_area("You:", key="user_input", on_change=submit_message, height=100)

# Display chat history
for chat in st.session_state.history:
    st.text_area("You:", chat["user"], height=100, key=f"user_{chat['user']}")
    st.text_area("Chatty:", chat["bot"], height=100, key=f"bot_{chat['bot']}", disabled=True)

import streamlit as st
import openai
import os

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure this is set in your environment variables

def get_response(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the appropriate model
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI
st.title("🌍Careconnect - Mental Health Chatbot")

# Define a state to store the chat history
if 'history' not in st.session_state:
    st.session_state.history = []

def submit_message():
    if st.session_state.user_input:
        messages = [{"role": "system", "content": "You are Chatty, a mental health support chatbot. Respond empathetically and supportively."}]
        messages.extend([{"role": "user", "content": chat["user"]} for chat in st.session_state.history])
        messages.append({"role": "user", "content": st.session_state.user_input})
        
        response = get_response(messages)
        st.session_state.history.append({"user": st.session_state.user_input, "bot": response})
        st.session_state.user_input = ""  # Clear input field after submission

# Text input for user message
st.text_input("You:", key="user_input", on_change=submit_message)

# Display chat history
for chat in st.session_state.history:
    st.text_area("You:", chat["user"], height=100, key=f"user_{chat['user']}", disabled=True)
    st.text_area("Chatty:", chat["bot"], height=100, key=f"bot_{chat['bot']}", disabled=True)


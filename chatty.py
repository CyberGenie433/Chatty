import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = 'your-openai-api-key'

# Define a function to get a response from GPT
def get_gpt_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # You can use gpt-3.5-turbo or gpt-4
        messages=messages,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

# Streamlit app code
st.title("Mental Health Chatbot")

# Initialize session state if not already done
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Create a text input for user to type messages
user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        # Add the user's message to the conversation history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get the response from GPT
        response = get_gpt_response(st.session_state.messages)
        
        # Add the bot's response to the conversation history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display the conversation
        conversation = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages])
        st.text_area("Conversation", value=conversation, height=300)
    else:
        st.warning("Please enter a message before clicking 'Send'.")

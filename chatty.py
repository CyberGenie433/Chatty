import streamlit as st
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_response(prompt):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # You can use other models like "gpt-3.5-turbo" if needed
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app layout
st.title("🌍 Careconnect")
st.write("Hello! I'm 🌍 Careconnect. How can I assist you today?")

# Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

# Display conversation history
for message in st.session_state.history:
    st.write(message)

# Input text from user
user_input = st.text_input("Your message:")

if st.button("Send"):
    if user_input:
        # Add user message to history
        st.session_state.history.append(f"User: {user_input}")
        
        # Create a prompt for the model
        history_text = "\n".join(st.session_state.history)
        prompt = f"{history_text}\n🌍 Careconnect:"
        
        # Get the response from OpenAI
        bot_response = get_openai_response(prompt)
        
        # Add bot response to history
        st.session_state.history.append(f"🌍 Careconnect: {bot_response}")
        
        # Display the response
        st.write(f"🌍 Careconnect: {bot_response}")
    else:
        st.write("Please enter a message to get a response.")

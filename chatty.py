import streamlit as st
import openai
import os
# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",  # You can use other models like "gpt-3.5-turbo" if needed
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Streamlit app layout
st.title("🌍 Careconnect Chatbot")
st.write("Hello! I'm 🌍 Careconnect. How can I assist you today?")

# Input text from user
user_input = st.text_input("Your message:")

if st.button("Send"):
    if user_input:
        # Create a prompt for the model
        prompt = f"User: {user_input}\n🌍 Careconnect:"
        
        # Get the response from OpenAI
        bot_response = get_openai_response(prompt)
        
        # Display the response
        st.write(f"🌍 Careconnect: {bot_response}")
    else:
        st.write("Please enter a message to get a response.")



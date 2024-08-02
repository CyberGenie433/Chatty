import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = 'your-openai-api-key'

# Define a function to get a response from GPT
def get_gpt_response(prompt):
    response = openai.Completion.create(
        model="gpt-4",  # You can use gpt-3.5-turbo or gpt-4
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()

# Streamlit app code
st.title("Mental Health Chatbot")

# Create a text input for user to type messages
user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        # Construct the prompt with context
        prompt = f"You are a supportive mental health chatbot. Respond empathetically and provide useful advice if appropriate. User: {user_input}"
        
        # Get the response from GPT
        response = get_gpt_response(prompt)
        
        # Display the response
        st.text_area("Bot:", value=response, height=150)
    else:
        st.warning("Please enter a message before clicking 'Send'.")



import streamlit as st
import openai

# Initialize OpenAI API key
openai.api_key = 'your-openai-api-key'

# Streamlit app
st.title("Chatty - Smart Question Answering")

# Get user input
user_input = st.text_input("Ask a question:")

if user_input:
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=user_input,
        max_tokens=150
    )
    answer = response.choices[0].text.strip()
    st.write("Answer:")
    st.write(answer)
else:
    st.write("Please enter a question.")

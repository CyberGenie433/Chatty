import streamlit as st
from transformers import pipeline

# Initialize the question-answering pipeline
qa_pipeline = pipeline("text-generation", model="gpt2")

# Streamlit app
st.title("Chatty - Simple Question Answering")

# Get user input
user_input = st.text_input("Ask a question:")

# Generate and display the answer
if user_input:
    response = qa_pipeline(user_input, max_length=100, num_return_sequences=1)[0]['generated_text']
    st.write("Answer:")
    st.write(response)
else:
    st.write("Please enter a question.")



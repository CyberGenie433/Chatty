import streamlit as st
from transformers import pipeline

# Initialize the question-answering pipeline with a larger model
qa_pipeline = pipeline("text-generation", model="gpt-3.5-turbo")

# Streamlit app
st.title("Chatty - Smart Question Answering")

# Get user input
user_input = st.text_input("Ask a question:")

# Generate and display the answer
if user_input:
    response = qa_pipeline(user_input, max_length=150, num_return_sequences=1)[0]['generated_text']
    st.write("Answer:")
    st.write(response)
else:
    st.write("Please enter a question.")

import streamlit as st
from transformers import pipeline

# Initialize the text-generation pipeline with GPT-3 (or a similar large model)
qa_pipeline = pipeline("text-generation", model="gpt2")  # You can use a larger model if available

# Streamlit app
st.title("Chatty - Smart Question Answering")

# Instructions for users
st.write("""
    **Welcome to Chatty!**  
    Ask me anything, and I'll do my best to provide a helpful response.  
    For example, you can ask: "What is the capital of France?" or "Explain the theory of relativity."
""")

# Input field and button
user_input = st.text_input("Type your question here:", "")

# Display processing spinner
if st.button('Get Answer'):
    if user_input:
        with st.spinner('Generating response...'):
            response = qa_pipeline(user_input, max_length=150, num_return_sequences=1)
            answer = response[0]['generated_text'].strip()
            
            # Display the response
            st.write("**Answer:**")
            st.write(answer)
    else:
        st.error("Please enter a question before submitting.")

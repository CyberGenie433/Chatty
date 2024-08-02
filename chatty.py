import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load pre-trained model and tokenizer
model_name = "gpt2"  # You can choose "gpt3", "gpt2-medium", "gpt2-large", or "gpt2-xl" based on your needs
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def generate_response(prompt):
    # Encode the input prompt
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    
    # Generate a response
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=150,  # Adjust the max length as needed
            num_return_sequences=1,
            no_repeat_ngram_size=2,  # Helps reduce repetition
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode the output and return the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Streamlit UI
st.title("Chatty - Your Friendly Chatbot")
st.write("Hey there! 🤗 I'm Chatty, your friendly chatbot. How can I help you today?")

# Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

# Input from user
user_input = st.text_input("You:", "")

if user_input:
    if user_input.lower() == 'quit':
        st.write("It was nice chatting with you! Feel free to refresh the page if you want to talk again. 😊")
    else:
        # Store user input and generate response
        st.session_state.history.append(f"You: {user_input}")
        response = generate_response(user_input)
        
        # Format response for a more human-like touch
        response = response.strip().capitalize()
        response = f"{response[0].upper()}{response[1:]}"
        
        st.session_state.history.append(f"Chatty: {response}")
        
        # Display conversation history with improved formatting
        for message in st.session_state.history:
            if message.startswith("You:"):
                st.write(f"<div style='text-align: left;'><b>{message}</b></div>", unsafe_allow_html=True)
            else:
                st.write(f"<div style='text-align: right;'><b>{message}</b></div>", unsafe_allow_html=True)

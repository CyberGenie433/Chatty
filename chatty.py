import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load pre-trained model and tokenizer
model_name = "gpt2"  # You can choose "gpt3", "gpt2-medium", "gpt2-large", or "gpt2-xl" based on your needs
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def generate_response(prompt, history):
    # Combine history with the latest prompt to provide context
    full_prompt = "\n".join(history + [prompt])
    inputs = tokenizer.encode(full_prompt, return_tensors='pt')
    
    # Generate a response
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=200,  # Adjust the max length as needed
            num_return_sequences=1,
            no_repeat_ngram_size=2,  # Helps reduce repetition
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode the output and return the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Streamlit UI
st.title("Chatty - Your Friendly Chatbot")
st.write("Hello! 🤗 I'm Chatty, your friendly chatbot. How can I help you today? Feel free to ask me anything!")

# Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

# Input from user
user_input = st.text_input("You:", "")

if user_input:
    if user_input.lower() == 'quit':
        st.write("It was great talking to you! 😊 Feel free to refresh the page to start a new conversation.")
    else:
        # Store user input
        st.session_state.history.append(f"You: {user_input}")
        
        # Generate response based on history
        response = generate_response(user_input, st.session_state.history)
        
        # Format response to look more conversational
        response = response.strip()
        if response:
            st.session_state.history.append(f"Chatty: {response}")
        
        # Display conversation history with improved formatting
        for message in st.session_state.history:
            if message.startswith("You:"):
                st.write(f"<div style='text-align: left;'><b>{message}</b></div>", unsafe_allow_html=True)
            else:
                st.write(f"<div style='text-align: right;'><b>{message}</b></div>", unsafe_allow_html=True)

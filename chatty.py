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
            max_length=100,  # Adjust the max length as needed
            num_return_sequences=1,
            no_repeat_ngram_size=2,  # Helps reduce repetition
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode the output and return the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Streamlit UI
st.title("Chatbot with GPT-2")

# Input from user
user_input = st.text_input("You:", "")

if user_input:
    response = generate_response(user_input)
    st.text_area("Chatbot:", value=response, height=150, max_chars=None, key=None)

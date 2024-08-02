import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from textblob import TextBlob
import torch

# Check if torch is available
print(f"Torch version: {torch.__version__}")

# Load pre-trained model and tokenizer
model_name = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def generate_response(prompt):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def correct_spelling(text):
    blob = TextBlob(text)
    return str(blob.correct())

def main():
    st.title("Chatbot with GPT-2")
    
    user_input = st.text_input("You:", "")
    
    if user_input:
        corrected_input = correct_spelling(user_input)
        st.write(f"Corrected Input: {corrected_input}")
        
        response = generate_response(corrected_input)
        st.write(f"Chatbot: {response}")

if __name__ == "__main__":
    main()


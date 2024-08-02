import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from textblob import TextBlob
import torch

# Check if torch is available
st.write(f"Torch version: {torch.__version__}")
st.write(f"CUDA available: {torch.cuda.is_available()}")

# Load pre-trained model and tokenizer
model_name = 'gpt2'
try:
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    st.write("Model and tokenizer loaded successfully.")
except Exception as e:
    st.write(f"Error loading model or tokenizer: {e}")

def generate_response(prompt):
    try:
        inputs = tokenizer.encode(prompt, return_tensors='pt')
        outputs = model.generate(inputs, max_length=150, num_return_sequences=1)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    except Exception as e:
        return f"Error generating response: {e}"

def correct_spelling(text):
    try:
        blob = TextBlob(text)
        return str(blob.correct())
    except Exception as e:
        return f"Error correcting spelling: {e}"

def main():
    st.title("Interactive Chatbot with GPT-2")
    
    user_input = st.text_input("You:", "")
    
    if user_input:
        with st.spinner("Correcting spelling..."):
            corrected_input = correct_spelling(user_input)
            st.write(f"Corrected Input: {corrected_input}")
        
        with st.spinner("Generating response..."):
            response = generate_response(corrected_input)
            st.write(f"Chatbot: {response}")

if __name__ == "__main__":
    main()

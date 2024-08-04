import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"  # You can use "gpt2-medium", "gpt2-large", or "gpt2-xl" for larger models

def load_model_and_tokenizer(model_name):
    try:
        model = GPT2LMHeadModel.from_pretrained(model_name)
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        return model, tokenizer
    except Exception as e:
        st.error(f"Error loading model or tokenizer: {e}")
        return None, None

model, tokenizer = load_model_and_tokenizer(model_name)

def generate_response(user_input):
    if model is None or tokenizer is None:
        return "Model or tokenizer not loaded."

    try:
        # Encode input text
        inputs = tokenizer.encode(user_input, return_tensors="pt")
        # Generate response
        outputs = model.generate(inputs, max_length=150, num_beams=5, early_stopping=True)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    except Exception as e:
        return f"Error generating response: {e}"

# Streamlit app
def main():
    st.title("Mental Health Chatbot")

    st.write("### Welcome to the Mental Health Chatbot")
    st.write("I'm here to listen. Type your message below and I'll do my best to respond.")

    # Input from user
    user_input = st.text_input("You:", "")

    if user_input:
        response_text = generate_response(user_input)
        st.write(f"**Chatbot:** {response_text}")

if __name__ == "__main__":
    main()


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

def generate_response(user_input, conversation_history):
    if model is None or tokenizer is None:
        return "Model or tokenizer not loaded."
    
    try:
        # Append user input to conversation history
        conversation_history.append(f"User: {user_input}")
        conversation_text = "\n".join(conversation_history)
        
        # Encode the conversation history
        inputs = tokenizer.encode(conversation_text, return_tensors="pt")
        
        # Generate response
        outputs = model.generate(
            inputs,
            max_length=500,          # Adjusted length to accommodate more context
            num_beams=5,
            no_repeat_ngram_size=2,
            top_p=0.92,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id,
            early_stopping=True
        )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract the latest response from the conversation
        response = response.split("\n")[-1].replace("User:", "").strip()
        conversation_history.append(f"Chatbot: {response}")
        
        return response
    except Exception as e:
        return f"Error generating response: {e}"

# Streamlit app
def main():
    st.title("Intelligent Mental Health Chatbot")
    st.write("### Welcome to the Intelligent Mental Health Chatbot")
    st.write("I'm here to listen. Type your message below and I'll do my best to respond.")
    
    # Initialize session state for conversation history
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    # Input from user
    user_input = st.text_input("You:", "")
    
    if user_input:
        response_text = generate_response(user_input, st.session_state.conversation_history)
        st.write(f"**Chatbot:** {response_text}")

if __name__ == "__main__":
    main()

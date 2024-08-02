pip install streamlit transformers textblob
import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from textblob import TextBlob

# Load pre-trained model and tokenizer
model_name = 'gpt2'  # You can replace 'gpt2' with other models if you have access
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def generate_response(prompt):
    # Encode the input prompt
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    
    # Generate a response from the model
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1)
    
    # Decode the generated response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def correct_spelling(text):
    # Correct spelling using TextBlob
    blob = TextBlob(text)
    return str(blob.correct())

def main():
    st.title("Chatbot with GPT-2")
    
    # Text input from the user
    user_input = st.text_input("You:", "")
    
    if user_input:
        corrected_input = correct_spelling(user_input)
        st.write(f"Corrected Input: {corrected_input}")
        
        response = generate_response(corrected_input)
        st.write(f"Chatbot: {response}")

if __name__ == "__main__":
    main()

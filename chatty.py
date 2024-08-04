import streamlit as st
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load pre-trained T5 model and tokenizer
model_name = "t5-small"  # You can use "t5-base" or "t5-large" for better performance
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

# Function to generate a response from the T5 model
def generate_response(user_input):
    input_text = f"chat: {user_input}"
    inputs = tokenizer.encode(input_text, return_tensors="pt")
    outputs = model.generate(inputs, max_length=150, num_beams=5, early_stopping=True)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

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


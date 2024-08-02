import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import sympy as sp

# Load pre-trained model and tokenizer
model_name = "gpt2"  # You can choose "gpt3", "gpt2-medium", "gpt2-large", or "gpt2-xl" based on your needs
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def solve_math_problem(problem):
    try:
        # Parse and solve the math problem
        expression = sp.sympify(problem)
        solution = sp.simplify(expression)
        return str(solution)
    except Exception as e:
        return "I'm sorry, I couldn't solve the math problem."

def generate_response(prompt, history):
    # Combine history with the latest prompt to provide context
    full_prompt = "\n".join(history + [prompt])
    
    # Encode the input prompt
    inputs = tokenizer.encode(full_prompt, return_tensors='pt')

    # Ensure the input length does not exceed model's maximum length
    max_length = tokenizer.model_max_length
    if inputs.size(1) > max_length:
        inputs = inputs[:, -max_length:]  # Truncate to the last `max_length` tokens

    # Generate a response with constraints to avoid verbosity
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=min(max_length, 150),  # Ensure generated length is within model limits
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            pad_token_id=tokenizer.eos_token_id,
            temperature=0.7,  # Control the randomness of responses
            top_k=50,  # Limit the number of tokens considered for generation
        )
    
    # Decode the output and return the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    return response

def is_math_problem(text):
    # Simple heuristic to detect if the input is a math problem
    math_keywords = ["solve", "calculate", "evaluate", "find"]
    return any(keyword in text.lower() for keyword in math_keywords) or any(char.isdigit() for char in text)

# Streamlit UI
st.title("Chatty - Your Friendly Chatbot")
st.write("Hello! 🤗 I'm Chatty, your friendly chatbot. You can ask me anything, including math problems!")

# Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

# Input from user
user_input = st.text_input("You:", "")

if user_input:
    if user_input.lower() == 'quit':
        st.write("It was great talking to you! 😊 Feel free to refresh the page to start a new conversation.")
    else:
        # Check if input is a math problem
        if is_math_problem(user_input):
            response = solve_math_problem(user_input)
        else:
            # Store user input
            st.session_state.history.append(f"You: {user_input}")
            
            # Generate response based on history
            response = generate_response(user_input, st.session_state.history)
            
            # Ensure response is not empty and format it
            if response:
                st.session_state.history.append(f"Chatty: {response}")
        
        # Display the response
        if response:
            st.session_state.history.append(f"Chatty: {response}")
        
        # Display conversation history with improved formatting
        for message in st.session_state.history:
            if message.startswith("You:"):
                st.write(f"<div style='text-align: left;'><b>{message}</b></div>", unsafe_allow_html=True)
            else:
                st.write(f"<div style='text-align: right;'><b>{message}</b></div>", unsafe_allow_html=True)

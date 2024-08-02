import streamlit as st
from transformers import pipeline
from sympy import sympify, solve, Eq

# Initialize the text-generation pipeline with GPT-2
qa_pipeline = pipeline("text-generation", model="gpt2")

# Streamlit app
st.title("Chatty")

# Instructions for users
st.write("""
    **Welcome to Chatty!**  
    How, can I help you
""")

# Input field and button
user_input = st.text_area("Type your question here:", "")

def evaluate_math_expression(expression):
    try:
        # Try to interpret the expression
        expr = sympify(expression)
        # If the expression is an equation, solve it
        if isinstance(expr, Eq):
            solutions = solve(expr)
            return f"Solutions: {solutions}"
        else:
            return f"Result: {expr}"
    except Exception as e:
        return f"Error: {e}"

def is_math_expression(expression):
    # Simple heuristic to determine if the input is likely a math expression
    math_keywords = ["solve", "integrate", "differentiate", "simplify", "expand"]
    operators = ["+", "-", "*", "/", "^"]
    return any(keyword in expression.lower() for keyword in math_keywords) or any(op in expression for op in operators)

# Display processing spinner and results
if st.button('Get Answer'):
    if user_input:
        with st.spinner('Processing...'):
            if is_math_expression(user_input):
                # Handle math expressions
                result = evaluate_math_expression(user_input)
                st.write("**Math Answer:**")
            else:
                # Handle general questions
                response = qa_pipeline(user_input, max_length=150, num_return_sequences=1)
                result = response[0]['generated_text'].strip()
                st.write("**General Answer:**")
            
            st.write(result)
    else:
        st.error("Please enter a question or expression before submitting.")

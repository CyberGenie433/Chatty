import streamlit as st
from sympy import sympify, solve, Eq
import openai

# Initialize OpenAI API key
openai.api_key = 'your-openai-api-key'  # Replace with your actual API key

# Streamlit app
st.title("Chatty - Your Smart Assistant")

# Instructions for users
st.write("""
    **Welcome to Chatty!**  
    You can ask me any type of question, and I'll do my best to provide a helpful response.  
    For math problems, I can solve them directly. For general questions, I'll use advanced language models to provide answers.
""")

# Input field
user_input = st.text_area("Type your question or math expression here:", "")

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

def get_general_answer(question):
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=question,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

# Button to get the answer
if st.button('Get Answer'):
    if user_input:
        with st.spinner('Processing your request...'):
            if is_math_expression(user_input):
                # Handle math expressions
                result = evaluate_math_expression(user_input)
                st.write("**Math Answer:**")
            else:
                # Handle general questions
                result = get_general_answer(user_input)
                st.write("**General Answer:**")
            
            st.write(result)
    else:
        st.error("Please enter a question or expression before submitting.")

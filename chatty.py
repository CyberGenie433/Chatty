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
    You can ask me general questions or enter mathematical expressions.  
    I'll automatically provide an answer. For math problems, I'll solve them directly. For other questions, I'll use advanced language models.
""")

# Input field
user_input = st.text_area("Type your question or math expression here:", "", height=150)

def evaluate_math_expression(expression):
    try:
        expr = sympify(expression)
        if isinstance(expr, Eq):
            solutions = solve(expr)
            return f"Solutions: {solutions}"
        else:
            return f"Result: {expr}"
    except Exception as e:
        return f"Error in math expression: {e}"

def is_math_expression(expression):
    # Determine if the input is likely a math expression
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
        return f"Error with OpenAI API: {e}"

# Process input automatically
if user_input:
    with st.spinner('Processing your request...'):
        if is_math_expression(user_input):
            result = evaluate_math_expression(user_input)
            st.subheader("Math Answer:")
        else:
            result = get_general_answer(user_input)
            st.subheader("General Answer:")
        
        st.write(result)
else:
    st.info("Please enter a question or expression above.")

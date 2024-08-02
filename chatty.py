import streamlit as st
from transformers import pipeline
from sympy import sympify, solve, Eq

# Initialize the text-generation pipeline with GPT-2
qa_pipeline = pipeline("text-generation", model="gpt2")

# Streamlit app
st.title("Chatty")

# Mode selection
mode = st.radio("Choose Mode:", ("General Q&A", "Math Solver"))

if mode == "General Q&A":
    # Instructions for users
    st.write("""
        **Welcome to Chatty Q&A!**  
        Ask me anything, and I'll do my best to provide a helpful response.  
        For example, you can ask: "What is the capital of France?" or "Explain the theory of relativity."
    """)
    
    # Input field and button
    user_input = st.text_input("Type your question here:", "")
    
    # Display processing spinner
    if st.button('Get Answer'):
        if user_input:
            with st.spinner('Generating response...'):
                response = qa_pipeline(user_input, max_length=150, num_return_sequences=1)
                answer = response[0]['generated_text'].strip()
                
                # Display the response
                st.write("**Answer:**")
                st.write(answer)
        else:
            st.error("Please enter a question before submitting.")

elif mode == "Math Solver":
    # Instructions for users
    st.write("""
        **Welcome to Chatty Math Solver!**  
        Enter a mathematical expression or equation below, and I'll solve it for you.  
        For example, you can enter: "2 + 2", "solve x^2 - 4 = 0", or "integrate x^2 dx".
    """)
    
    # Input field and button
    user_input = st.text_area("Type your math question or expression here:", "")
    
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
    
    # Display processing spinner and results
    if st.button('Get Answer'):
        if user_input:
            with st.spinner('Processing...'):
                result = evaluate_math_expression(user_input)
                st.write("**Answer:**")
                st.write(result)
        else:
            st.error("Please enter a math expression or question before submitting.")

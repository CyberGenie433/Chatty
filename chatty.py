import streamlit as st

# Set the title of the app
st.title("Welcome to My First Streamlit App")

# Add a text input
name = st.text_input("Enter your name:")

# Display the name entered by the user
if name:
    st.write(f"Hello, {name}! Welcome to the app.")

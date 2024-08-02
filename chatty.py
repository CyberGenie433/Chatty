import streamlit as st

# Streamlit app
st.title("Chatty - Simple Text Echo")

# Get user input
user_input = st.text_input("Enter text:")

# Display the input text as output
if user_input:
    st.write("You entered:")
    st.write(user_input)
else:
    st.write("Please enter some text.")


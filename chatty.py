import streamlit as st

st.title("_Streamlit_ is :red[cool] :sunglasses:")

user_input = st.text_input("Enter a prompt")
st.write("Hello",user_input,"what can I help you with?")

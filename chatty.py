import streamlit as st

st.title("_Streamlit_ is :blue[cool] :sunglasses:")

name = st.text_input("Enter your name:")

st.header("This is a header with a divider", divider="gray")
st.header("These headers have rotating dividers", divider=True)
st.header("One", divider=True)
st.header("Two", divider=True)
st.header("Three", divider=True)
st.header("Four", divider=True)

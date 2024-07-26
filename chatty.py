import streamlit as st

st.title("_Streamlit_ is :red[cool] :sunglasses:")

name = st.text_input("Enter your name:")

st.json(
    {
        "foo": "bar",
        "baz": "boz",
        "stuff": [
            "stuff 1",
            "stuff 2",
            "stuff 3",
            "stuff 5",
        ],
    }
)

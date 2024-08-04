import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("Streamlit st.write() Demonstration")

# Writing text
st.write("## This is a header")
st.write("This is a simple text example using `st.write()`.")

# Writing dataframes
data = {
    "Column 1": [1, 2, 3, 4],
    "Column 2": [10, 20, 30, 40]
}

# Validate data
if isinstance(data, dict) and all(isinstance(v, list) for v in data.values()):
    try:
        df = pd.DataFrame(data)
        st.write("### Here is a dataframe")
        st.write(df)
    except Exception as e:
        st.write(f"Error creating DataFrame: {e}")
else:
    st.write("Data format is incorrect. Ensure data is a dictionary with lists as values.")

# Writing charts
st.write("### Here is a chart")
try:
    fig, ax = plt.subplots()
    ax.plot(df["Column 1"], df["Column 2"])
    st.pyplot(fig)  # Use st.pyplot for Matplotlib figures
except Exception as e:
    st.write(f"Error creating chart: {e}")

# Writing markdown
st.write("### This is markdown")
st.write("""
* Item 1
* Item 2
* Item 3
""")

# Writing a dictionary
st.write("### Here is a dictionary")
st.write({"name": "Tommy", "age": 10})


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("Streamlit st.write() Demonstration")

# Writing text
st.write("## This is a header")
st.write("This is a simple text example using `st.write()`.")

# Simplified and validated data for DataFrame
data = {
    "Column 1": [1, 2, 3, 4],
    "Column 2": [10, 20, 30, 40]
}

# Initialize DataFrame as None
df = None

# Validate and create DataFrame
try:
    # Check if data is a dictionary and all values are lists of the same length
    if isinstance(data, dict) and all(isinstance(v, list) for v in data.values()):
        df = pd.DataFrame(data)
        st.write("### Here is a dataframe")
        st.write(df)
    else:
        st.write("Data format is incorrect. Ensure data is a dictionary with lists as values.")
except Exception as e:
    st.write(f"Error creating DataFrame: {e}")

# Writing charts
st.write("### Here is a chart")
if df is not None:
    try:
        fig, ax = plt.subplots()
        ax.plot(df["Column 1"], df["Column 2"], marker='o')
        ax.set_xlabel('Column 1')
        ax.set_ylabel('Column 2')
        ax.set_title('Column 1 vs Column 2')
        st.pyplot(fig)  # Use st.pyplot for Matplotlib figures
    except Exception as e:
        st.write(f"Error creating chart: {e}")
else:
    st.write("DataFrame was not created, so the chart cannot be displayed.")

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


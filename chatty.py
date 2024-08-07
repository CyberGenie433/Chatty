import streamlit as st
import openai
from langchain_community.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize LangChain components
llm = OpenAI(model_name="text-davinci-003", openai_api_key=openai.api_key)

# Define the prompt template for conversation
prompt_template = ChatPromptTemplate(
    system_message="You are 🌍 Careconnect, a helpful assistant.",
    user_message="{user_input}",
    assistant_message="{bot_response}"
)

# Create the conversation chain
conversation_chain = ConversationChain(
    llm=llm,
    prompt_template=prompt_template,
    history_length=5  # Adjust based on how many past interactions to keep
)

# Streamlit app layout
st.title("🌍 Careconnect Chatbot")
st.write("Hello! I'm 🌍 Careconnect. How can I assist you today?")

# Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

# Display conversation history
for message in st.session_state.history:
    st.write(message)

# Input text from user
user_input = st.text_input("Your message:")

if st.button("Send"):
    if user_input:
        # Add user message to history
        st.session_state.history.append(f"User: {user_input}")
        
        # Get the response from LangChain
        bot_response = conversation_chain.run(user_input)
        
        # Add bot response to history
        st.session_state.history.append(f"🌍 Careconnect: {bot_response}")
        
        # Display the response
        st.write(f"🌍 Careconnect: {bot_response}")
    else:
        st.write("Please enter a message to get a response.")


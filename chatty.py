import streamlit as st
import openai
import os

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure to set this in your environment variables

def get_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use appropriate engine
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI
st.title("Chatty - Mental Health Chatbot")

# Define a state to store the chat history
if 'history' not in st.session_state:
    st.session_state.history = []

def submit_message():
    if st.session_state.user_input:
        prompt = f"You are Chatty, a mental health support chatbot. Respond empathetically and supportively to the following message: {st.session_state.user_input}"
        response = get_response(prompt)
        st.session_state.history.append({"user": st.session_state.user_input, "bot": response})
        st.session_state.user_input = ""  # Clear input field after submission

# Add a text area for user input
st.text_area("You:", key="user_input", height=100)

# JavaScript for handling Enter key press
st.markdown("""
<script>
const textarea = document.querySelector('textarea');
textarea.addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        window.parent.postMessage({type: 'submit_message'}, '*');
    }
});
</script>
""", unsafe_allow_html=True)

# Handle the message submission
if st.session_state.get('message_submitted', False):
    submit_message()
    st.session_state['message_submitted'] = False

# Display chat history
for chat in st.session_state.history:
    st.text_area("You:", chat["user"], height=100, key=f"user_{chat['user']}")
    st.text_area("Chatty:", chat["bot"], height=100, key=f"bot_{chat['bot']}", disabled=True)

# JavaScript to handle the message submission
st.markdown("""
<script>
window.addEventListener('message', function(event) {
    if (event.data.type === 'submit_message') {
        document.querySelector('textarea').dispatchEvent(new Event('change'));
        window.parent.postMessage({type: 'message_submitted'}, '*');
    }
});
</script>
""", unsafe_allow_html=True)

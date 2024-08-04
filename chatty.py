import streamlit as st
import openai

# Load OpenAI API key from secrets
openai.api_key = st.secrets.get("OPENAI_API_KEY")

def generate_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # or use "text-davinci-002" or other available models
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response."

def main():
    st.title("GPT-3 Specific Answer Chatbot")

    st.write("Ask a specific question below. The chatbot will provide an answer using GPT-3.")

    user_input = st.text_input("You:", "")
    
    if user_input:
        prompt = f"Provide a specific and accurate answer to the following question: {user_input}"
        response_text = generate_response(prompt)
        st.write(f"**Chatbot:** {response_text}")

if __name__ == "__main__":
    main()

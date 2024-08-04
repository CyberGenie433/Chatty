import streamlit as st
import openai
import requests

# Load API keys from secrets
openai.api_key = st.secrets.get("OPENAI_API_KEY")
BING_SEARCH_API_KEY = st.secrets.get("BING_SEARCH_API_KEY")

# Function to perform web search
def search_web(query):
    if not BING_SEARCH_API_KEY:
        return "API key not found."
    
    headers = {"Ocp-Apim-Subscription-Key": BING_SEARCH_API_KEY}
    params = {"q": query, "count": 5}
    try:
        response = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        if "webPages" in search_results and search_results["webPages"]["value"]:
            snippets = [result["snippet"] for result in search_results["webPages"]["value"]]
            return " ".join(snippets)
        return "No relevant information found."
    except Exception as e:
        return f"Error fetching search results: {e}"

# Function to generate response using GPT-3
def generate_response(prompt, web_data):
    try:
        # Create a prompt for GPT-3 with web search results
        full_prompt = f"Based on the following information: {web_data}\n\nAnswer the question: {prompt}"
        response = openai.Completion.create(
            model="text-davinci-003",  # Use "text-davinci-003" or "gpt-4" if available
            prompt=full_prompt,
            max_tokens=150,
            temperature=0.7,
            stop=["\n"]
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response."

def main():
    st.title("Enhanced Chatbot with Web Search")

    st.write("Ask a specific question below. The chatbot will search the web for information and provide an answer.")

    user_input = st.text_input("You:", "")
    
    if user_input:
        # Perform web search
        web_data = search_web(user_input)
        
        # Generate a response based on web search results
        response_text = generate_response(user_input, web_data)
        st.write(f"**Chatbot:** {response_text}")

if __name__ == "__main__":
    main()

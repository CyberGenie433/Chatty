import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import requests

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Function to get API key from Streamlit secrets or environment variables
def get_api_key():
    try:
        # Try to retrieve the API key from Streamlit secrets
        api_key = st.secrets["bing"]["api_key"]
        if not api_key:
            raise ValueError("API key is empty.")
        return api_key
    except KeyError:
        st.error("API key is not found in Streamlit secrets.")
        return None
    except ValueError as e:
        st.error(str(e))
        return None

# Function to search the web using Bing Search API
def search_web(query):
    api_key = get_api_key()
    if not api_key:
        return "API key is not configured properly."
    
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query, "count": 5}
    try:
        response = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        if "webPages" in search_results and search_results["webPages"]["value"]:
            snippets = [result["snippet"] for result in search_results["webPages"]["value"]]
            return " ".join(snippets)
        return "No relevant information found."
    except requests.RequestException as e:
        st.error(f"Error fetching search results: {e}")
        return "Failed to fetch search results."

# Function to generate a response using GPT-2
def generate_response(prompt, web_data=None):
    refined_prompt = f"Provide a detailed and accurate answer to the following question: {prompt}"
    if web_data:
        refined_prompt = f"Based on the following information: {web_data}\n\n{refined_prompt}"
    
    inputs = tokenizer.encode(refined_prompt, return_tensors="pt")
    
    try:
        outputs = model.generate(
            inputs,
            max_length=150,
            num_beams=5,
            no_repeat_ngram_size=2,
            top_p=0.92,
            temperature=0.7,  # Adjust temperature for better coherence
            pad_token_id=tokenizer.eos_token_id,
            early_stopping=True
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.replace(refined_prompt, "").strip()
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response."

# Streamlit app function
def main():
    st.title("Enhanced GPT-2 Chatbot")

    st.write("Ask a specific question below, and the chatbot will respond using GPT-2. Optionally, it can use web search data for better accuracy.")

    user_input = st.text_input("You:", "")
    
    if user_input:
        # Perform web search if applicable
        if "search" in user_input.lower():
            query = user_input.replace("search", "").strip()
            web_data = search_web(query)
            response_text = generate_response(query, web_data)
        else:
            response_text = generate_response(user_input)
        
        st.write(f"**Chatbot:** {response_text}")

if __name__ == "__main__":
    main()

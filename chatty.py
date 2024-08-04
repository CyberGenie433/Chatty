import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import requests

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Access API key from Streamlit secrets
BING_SEARCH_API_KEY = st.secrets.get("bing", {}).get("api_key")

# Bing Search API setup
BING_SEARCH_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"

def search_web(query):
    if not BING_SEARCH_API_KEY:
        return "API key not found."
    
    headers = {"Ocp-Apim-Subscription-Key": BING_SEARCH_API_KEY}
    params = {"q": query, "count": 5}
    try:
        response = requests.get(BING_SEARCH_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        if "webPages" in search_results and search_results["webPages"]["value"]:
            snippets = [result["snippet"] for result in search_results["webPages"]["value"]]
            return " ".join(snippets)
        return "No relevant information found."
    except Exception as e:
        return f"Error fetching search results: {e}"

def generate_response(prompt, web_data):
    full_prompt = f"Based on the following information: {web_data}\n\nAnswer the question: {prompt}"
    inputs = tokenizer.encode(full_prompt, return_tensors="pt")
    try:
        outputs = model.generate(
            inputs,
            max_length=150,
            num_beams=5,
            no_repeat_ngram_size=2,
            top_p=0.92,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id,
            early_stopping=True
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response."

def main():
    st.title("GPT-2 Enhanced Chatbot with Web Search")

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

import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import requests

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"

def load_model_and_tokenizer(model_name):
    try:
        model = GPT2LMHeadModel.from_pretrained(model_name)
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        return model, tokenizer
    except Exception as e:
        st.error(f"Error loading model or tokenizer: {e}")
        return None, None

model, tokenizer = load_model_and_tokenizer(model_name)

# Fetch API key from secrets
BING_SEARCH_API_KEY = st.secrets.get("BING_SEARCH_API_KEY")

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

def generate_response(user_input):
    if model is None or tokenizer is None:
        return "Model or tokenizer not loaded."
    
    try:
        prompt = f"Answer the following question: {user_input}"
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        outputs = model.generate(
            inputs,
            max_new_tokens=150,  # Fixed response length for simplicity
            num_beams=5,
            no_repeat_ngram_size=2,
            top_p=0.92,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.replace(prompt, "").strip() or "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"Error generating response: {e}"

def main():
    st.title("Simplified Chatbot")

    st.write("Ask a question below. Specify 'search' to look up information online.")

    user_input = st.text_input("You:", "")
    
    if user_input:
        if "search" in user_input.lower():
            query = user_input.replace("search", "").strip()
            external_info = search_web(query)
            st.write(f"**Chatbot (Web Info):** {external_info}")
        else:
            response_text = generate_response(user_input)
            st.write(f"**Chatbot:** {response_text}")

if __name__ == "__main__":
    main()

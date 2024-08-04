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

# Bing Search API setup
BING_SEARCH_API_KEY = st.secrets["BING_SEARCH_API_KEY"]
BING_SEARCH_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"

def search_web(query):
    headers = {"Ocp-Apim-Subscription-Key": BING_SEARCH_API_KEY}
    params = {"q": query, "count": 5}
    try:
        response = requests.get(BING_SEARCH_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        return search_results
    except Exception as e:
        st.error(f"Error fetching search results: {e}")
        return {}

def generate_response(user_input, response_type):
    if model is None or tokenizer is None:
        return "Model or tokenizer not loaded."
    
    try:
        # Prepare the input prompt
        prompt = f"Answer the following question: {user_input}"
        
        # Encode the input prompt
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        
        # Generate response
        max_new_tokens = 150 if response_type == "brief" else 1024
        outputs = model.generate(
            inputs,
            max_new_tokens=max_new_tokens,  # Limit response length
            num_beams=5,
            no_repeat_ngram_size=2,
            top_p=0.92,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id,
            early_stopping=True
        )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Ensure the response addresses the user query
        response = response.replace(prompt, "").strip()
        
        return response if response else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"Error generating response: {e}"

def get_external_information(query):
    search_results = search_web(query)
    if "webPages" in search_results and search_results["webPages"]["value"]:
        snippets = [result["snippet"] for result in search_results["webPages"]["value"]]
        return " ".join(snippets)
    return "No relevant information found."

# Streamlit app
def main():
    st.title("Focused Chatbot")

    st.write("### Welcome to the Focused Chatbot")
    st.write("Ask a specific question below. Specify 'brief' for short answers or 'detailed' for long answers.")

    # Initialize session state for conversation history
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    # Input from user
    user_input = st.text_input("You:", "")
    
    if user_input:
        response_type = "brief" if "brief" in user_input.lower() else "detailed"
        
        if "search" in user_input.lower():
            query = user_input.replace("search", "").strip()
            external_info = get_external_information(query)
            st.write(f"**Chatbot (Web Info):** {external_info}")
        else:
            response_text = generate_response(user_input, response_type)
            st.write(f"**Chatbot:** {response_text}")

if __name__ == "__main__":
    main()

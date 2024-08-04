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
BING_SEARCH_API_KEY = "YOUR_BING_SEARCH_API_KEY"
BING_SEARCH_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"

def search_web(query):
    headers = {"Ocp-Apim-Subscription-Key": BING_SEARCH_API_KEY}
    params = {"q": query, "count": 5}
    response = requests.get(BING_SEARCH_ENDPOINT, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    return search_results

def generate_response(user_input, conversation_history):
    if model is None or tokenizer is None:
        return "Model or tokenizer not loaded."
    
    try:
        # Append user input to conversation history
        conversation_history.append(f"User: {user_input}")
        conversation_text = "\n".join(conversation_history)
        
        # Encode the conversation history
        inputs = tokenizer.encode(conversation_text, return_tensors="pt")
        
        # Generate response
        outputs = model.generate(
            inputs,
            max_new_tokens=1024,  # Allowing up to 1024 new tokens in the response
            num_beams=5,
            no_repeat_ngram_size=2,
            top_p=0.92,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id,
            early_stopping=True
        )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract the latest response from the conversation
        response = response.split("\n")[-1].replace("User:", "").strip()
        conversation_history.append(f"Chatbot: {response}")
        
        return response
    except Exception as e:
        return f"Error generating response: {e}"

def get_external_information(query):
    search_results = search_web(query)
    if "webPages" in search_results:
        snippets = [result["snippet"] for result in search_results["webPages"]["value"]]
        return " ".join(snippets)
    return "No relevant information found."

# Streamlit app
def main():
    st.title("Smart Chatbot with Web Integration")

    st.write("### Welcome to the Smart Chatbot")
    st.write("I'm here to assist you and can look up information from the web if needed. Type your message below.")

    # Initialize session state for conversation history
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    # Input from user
    user_input = st.text_input("You:", "")
    
    if user_input:
        # Check if user input requires web search
        if "search" in user_input.lower():
            query = user_input.replace("search", "").strip()
            external_info = get_external_information(query)
            st.write(f"**Chatbot (Web Info):** {external_info}")
        else:
            response_text = generate_response(user_input, st.session_state.conversation_history)
            st.write(f"**Chatbot:** {response_text}")

if __name__ == "__main__":
    main()

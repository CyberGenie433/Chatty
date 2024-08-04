import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

def generate_response(prompt):
    # Refine the prompt with additional context
    refined_prompt = f"Provide a concise and accurate answer to the following question: {prompt}"
    
    # Encode the prompt
    inputs = tokenizer.encode(refined_prompt, return_tensors="pt")
    
    try:
        # Generate a response from GPT-2
        outputs = model.generate(
            inputs,
            max_length=150,  # Adjust if needed
            num_beams=5,
            no_repeat_ngram_size=2,
            top_p=0.92,
            temperature=0.6,  # Lower temperature for more focused responses
            pad_token_id=tokenizer.eos_token_id,
            early_stopping=True
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Ensure response is trimmed and clean
        return response.replace(refined_prompt, "").strip()
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response."

def main():
    st.title("GPT-2 Chatbot")

    st.write("Ask a specific question below, and the chatbot will respond using GPT-2.")

    user_input = st.text_input("You:", "")
    
    if user_input:
        response_text = generate_response(user_input)
        st.write(f"**Chatbot:** {response_text}")

if __name__ == "__main__":
    main()

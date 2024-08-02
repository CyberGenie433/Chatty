from transformers import pipeline

# Load a pre-trained model
chatbot = pipeline("conversational")

def get_response(user_input):
    # Generate a response from the chatbot
    response = chatbot(user_input)
    return response[0]['generated_text']

# Example usage
user_query = "What is the capital of France?"
print(get_response(user_query))

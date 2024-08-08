from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Set your OpenAI API key
llm = OpenAI(api_key='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')

# Define the prompt template for conversation
prompt_template = ChatPromptTemplate(
    system_message="You are 🌍 Careconnect, a helpful assistant.",
    user_message="{user_input}",
    assistant_message="{bot_response}"
)



# Streamlit app layout
st.title("🌍 Careconnect Chatbot")
st.write("Hello! I'm 🌍 Careconnect. How can I assist you today?")

if user_input:
        try:
            # Add user message to history
            st.session_state.history.append(f"User: {user_input}")
            
            # Get the response from LangChain
            bot_response = conversation_chain.run(user_input)
            
            # Add bot response to history
            st.session_state.history.append(f"🌍 Careconnect: {bot_response}")
            
            # Display the response
            st.write(f"🌍 Careconnect: {bot_response}")
        except Exception as e:
            st.write(f"An error occurred: {e}")
else:
        st.write("Please enter a message to get a response.")

# Define a prompt template for querying
prompt_template = PromptTemplate(
    input_variables=["data_description", "question"],
    template="""
    You are a data analyst. Make your answers are easy to understand by a 10 year old. Here is the data you have:
    {data_description}

    Based on this data, answer the question: {question}
    """
)

# Create a LangChain
chain = LLMChain(llm=llm, prompt=prompt_template)

def get_response(data_description, question):
    # Running the chain to get a response based on the data description and a question
    response = chain.run(data_description=data_description, question=question)
    return response

# Example usage
if __name__ == "__main__":
    data_description = "Data includes various facts about countries, such as capitals and population sizes and hurricane data"
    while True:
        question = input("Enter A Question \n")
        answer = get_response(data_description, question)

        print(answer)

        if question == "exit":

            break






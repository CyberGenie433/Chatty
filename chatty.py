from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
import streamlit as st

# Set your OpenAI API key
llm = OpenAI(openai_api_key='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')

# Define the prompt template for conversation
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are 🌍 Careconnect, a helpful assistant."),
    ("user", "{user_input}"),
    ("assistant", "{bot_response}")
])

# Define a prompt template for querying
query_prompt_template = PromptTemplate(
    input_variables=["data_description", "question"],
    template="""
    You are a data analyst. Make your answers easy to understand by a 10-year-old. Here is the data you have:
    {data_description}

    Based on this data, answer the question: {question}
    """
)

# Create a LangChain for conversation and querying
conversation_chain = LLMChain(llm=llm, prompt=prompt_template)
query_chain = LLMChain(llm=llm, prompt=query_prompt_template)

# Streamlit app layout
st.title("🌍 Careconnect Chatbot")
st.write("Hello! I'm 🌍 Careconnect. How can I assist you today?")

# Input field
user_input = st.text_input("Enter your message:")

if user_input:
    try:
        # Get the response from LangChain
        bot_response = conversation_chain.run(user_input=user_input)
        
        # Display the response
        st.write(f"🌍 Careconnect: {bot_response}")
    except Exception as e:
        st.write(f"An error occurred: {e}")
else:
    st.write("Please enter a message to get a response.")

# Example usage in console
if __name__ == "__main__":
    data_description = "Data includes various facts about countries, such as capitals and population sizes and hurricane data."
    while True:
        question = input("Enter A Question: \n")
        if question.lower() == "exit":
            break

        answer = query_chain.run(data_description=data_description, question=question)
        print(answer)

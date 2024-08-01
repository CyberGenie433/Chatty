import streamlit as st
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

st.title("_Streamlit_ is :red[cool] :sunglasses:")

user_input = {["hello, i am",
user_input = st.text_input("Enter ")
st.write("Hello",user_input,"what can I help you with?")


# Initialize the OpenAI model with your API key
llm = OpenAI(api_key='sk-None-V0kN27JXPsXE2lCLZ2fBT3BlbkFJaBkL9arc9rvA4sgjGHEg')

# Define a prompt template for querying
prompt_template = PromptTemplate(
    input_variables=["data_description", "question"],
    template="""
    You are a data analyst. Here is the data you have:
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

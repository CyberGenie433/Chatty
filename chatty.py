import streamlit as st
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.title("_Streamlit_ is :red[cool] :sunglasses:")

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

file_path = 'health_stats.csv'
text_data = pd.read_csv(file_path)

# Ensure numerical data is parsed correctly
def parse_value(value):
    if isinstance(value, str):
        if '/' in value:
            return float(value.split('/')[0])
        elif ' years' in value:
            return float(value.split()[0])
        elif '%' in value:
            return float(value.strip('%'))
    return float(value)

text_data['Value'] = text_data['Value'].apply(parse_value)

# Initialize the OpenAI model
llm = OpenAI(api_key='sk-None-V0kN27JXPsXE2lCLZ2fBT3BlbkFJaBkL9arc9rvA4sgjGHEg')

# Define the prompt template for health statistics data
prompt_template = PromptTemplate(
    input_variables=["data_description", "question"],
    template="""
    You are a data analyst. You have access to the following health statistics data:
    {data_description}

    Question: {question}

    Please provide a detailed answer based on the data.
    """
)

# Create the LangChain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Function to generate data description for the health statistics
def generate_data_description():
    sample_entries = text_data.sample(min(len(text_data), 5))  # Get up to 5 random rows
    description = "The dataset contains various health statistics over different years. It includes data points such as Infant Mortality Rate, Life Expectancy, Maternal Mortality Rate, Prevalence of Diabetes, and Prevalence of Hypertension. The data is structured with the following columns:\n"
    description += "- Year: The year in which the statistic was recorded.\n"
    description += "- Statistic Type: The type of health statistic.\n"
    description += "- Value: The value of the statistic, which can be a rate, percentage, or a numerical value.\n\n"
    description += "Example entries:\n"
    description += "\n".join(f"Year: {row['Year']}, Statistic Type: {row['Statistic Type']}, Value: {row['Value']}" for _, row in sample_entries.iterrows())
    return description

def get_response(question):
    data_description = generate_data_description()
    response = chain.run(data_description=data_description, question=question)
    return response

# Function to plot the data
def plot_data(statistic_type):
    filtered_data = text_data[text_data['Statistic Type'] == statistic_type]
    if not filtered_data.empty:
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=filtered_data, x='Year', y='Value', marker='o')
        plt.title(f'{statistic_type} Over Time')
        plt.xlabel('Year')
        plt.ylabel(statistic_type)
        plt.xticks(rotation=45)
        plt.show()
    else:
        print(f"No data available for {statistic_type}")

# Allow for dynamic input via user prompt
if __name__ == "__main__":
    while True:
        user_input = input("Please enter your question or type 'exit' to quit, or type 'plot' to create a plot: ")
        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'plot':
            statistic_type = input("Enter the statistic type you want to plot (e.g., 'Infant Mortality Rate'): ")
            plot_data(statistic_type)
        else:
            answer = get_response(user_input)
            print("Answer:", answer)


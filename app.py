# Import necessary libraries
import streamlit as st
import openai
import os
from io import StringIO
import pandas as pd
from langchain.chains import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.chains.router import MultiPromptChain
from langchain.llms import OpenAI

from io import StringIO
from langchain.document_loaders.csv_loader import CSVLoader

# Make sure to add your OpenAI API key in the advanced settings of Streamlit's deployment
open_AI_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = open_AI_key

# Assuming you have the LangChain and financial route setup code here
# ... (your existing LangChain and route setup code)


def loadCSVFile(uploaded_file):
    

    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)

    text = df.to_string(index=False)
    return text

# Define the main function of the Streamlit app
def main():
    st.header("Welcome to FiniBot Financial Advisory! Please upload your financial spreadsheet. [Link to template]")

    # File uploader for the spreadsheet
    uploaded_file = st.file_uploader("Upload spreadsheet", type=['csv', 'xlsx'])
    
    # Radio button for selecting experience level
    experience_level = st.radio("Select your experience level:", ("Novice", "Expert"))

    # Display the spreadsheet if uploaded
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)  # Adjust this line if your spreadsheet is in a different format
        st.dataframe(df)  # Displaying the spreadsheet

        text = loadCSVFile(uploaded_file)

        print(text)

        # Process the spreadsheet and generate financial analysis
        analysis, recommendation = process_spreadsheet(df, experience_level)
        
        # Display the analysis and recommendation
        st.markdown("### FiniBot Analysis and Recommendation")
        st.markdown(f"**Analysis:** {analysis}")
        st.markdown(f"**Recommendation:** {recommendation}")

# Function to process the spreadsheet and generate analysis and recommendation
# Integrate the logic from your Jupyter notebook here.
def process_spreadsheet(df, experience_level):
    # Process the dataframe as per the logic in the Jupyter notebook
    # Include LangChain and routing logic here
    # ...

    analysis = "Analysis based on the spreadsheet data."
    recommendation = "Recommendation based on the analysis."
    return analysis, recommendation

if __name__ == "__main__":
    main()

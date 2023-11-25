# Import necessary libraries
import streamlit as st
import openai
import os
from io import StringIO
import pandas as pd



# Make sure to add your OpenAI API key in the advanced settings of streamlit's deployment
open_AI_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = open_AI_key






### Here, with some adjustments, copy-paste the code you developed for Question 1 in Assignment 3 
##########################################################################  
# Function to load and process the CSV file
# Function to load and process the CSV file
def loadCSVFile(df):
    # Convert fields to numeric, setting errors='coerce' will convert non-numeric values to NaN
    df['savings'] = pd.to_numeric(df['savings'], errors='coerce')
    df['credit_card_debt'] = pd.to_numeric(df['credit_card_debt'], errors='coerce')
    df['income'] = pd.to_numeric(df['income'], errors='coerce')

    # Fill NaN values with 0 or some default value
    df.fillna(0, inplace=True)

    # Extract required fields
    savings = df['savings'].iloc[0]
    credit_card_debt = df['credit_card_debt'].iloc[0]
    income = df['income'].iloc[0]

    # Format the extracted data
    formatted_text = f"savings: ${savings:.2f}\ncredit card debt: ${credit_card_debt:.2f}\nincome: ${income:.2f}"
    return formatted_text


# Function to process the spreadsheet and generate analysis and recommendation
def process_spreadsheet(df, experience_level):
    # Implement your specific business logic here
    analysis = "Analysis based on the spreadsheet data."
    recommendation = "Recommendation based on the analysis."
    return analysis, recommendation

# Define the main function of the Streamlit app
def main():
    st.header("Welcome to FiniBot Financial Advisory! Please upload your financial spreadsheet. [Link to template]")

    # File uploader for the spreadsheet
    uploaded_file = st.file_uploader("Upload spreadsheet", type=['csv', 'xlsx'])

    # Radio button for selecting experience level
    experience_level = st.radio("Select your experience level:", ("Novice", "Expert"))

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            processed_text = loadCSVFile(df)
            st.text(processed_text)

            # Process the spreadsheet and generate financial analysis
            analysis, recommendation = process_spreadsheet(df, experience_level)

            # Display the analysis and recommendation
            st.markdown("### FiniBot Analysis and Recommendation")
            st.markdown(f"**Analysis:** {analysis}")
            st.markdown(f"**Recommendation:** {recommendation}")

        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    main()
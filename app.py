# Import necessary libraries
import streamlit as st
import openai
import os
from io import StringIO
import pandas as pd



# Make sure to add your OpenAI API key in the advanced settings of streamlit's deployment
open_AI_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = open_AI_key



from langchain.document_loaders.csv_loader import CSVLoader

def loadCSVFile(csv_path):
  loader = CSVLoader(csv_path)
  data = loader.load()
  text = data[0].page_content
  return text

def run10times(csv_file):
    for _ in range(10):
      # Run the chain
        result = chain.run(csv_file)

# Print the result
print(result)

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

        # Process the spreadsheet and generate financial analysis
        analysis, recommendation = process_spreadsheet(df, experience_level)
        
        # Display the analysis and recommendation
        st.markdown("### FiniBot Analysis and Recommendation")
        st.markdown(f"**Analysis:**\n{analysis}")
        st.markdown(f"**Recommendation:**\n{recommendation}")

# Function to process the spreadsheet and generate analysis and recommendation


if __name__ == "__main__":
    main()

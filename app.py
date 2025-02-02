import streamlit as st
import os
import pandas as pd
from io import StringIO
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain, LLMChain
from langchain.chains.router import MultiPromptChain, LLMRouterChain
from langchain.chains.router.llm_router import RouterOutputParser
import openai
import tempfile
import shutil

from langchain.document_loaders.csv_loader import CSVLoader

print(os.environ.get("OPENAI_API_KEY"))

open_AI_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = open_AI_key






Output_template = """
 Format the output nicely into this template.

------------
 Summary
------------

 - Total savings:  {input}
 - Monthly debt: {input}
 - Monthly income: {input}

------------
 Financial situation:
 ------------


------------
Recommendation:
------------




"""
# Define your investment and debt templates (placeholders here)
investment_template ="""
You are a highly knowledgeable investment advisor. You excel at providing clear and succinct advice on financial matters. When faced with a question you're unsure about, you honestly acknowledge your uncertainty.
advise to invest  money and provide an investment portfolio based on savings and using 5 stocks.
Give advice based on the following details: {input}

""" + Output_template


debt_template= """
You are a courteous and considerate debt advisor. Your approach involves tactfully and sensitively informing clients about their financial situations, avoiding any guilt-tripping. You then transition into planning mode, creating a strategy for clients to pay off their debts. This plan includes allocating 10% of their income for monthly debt payments.

Here's the details provided {input}

""" + Output_template


def get_llm():
    #openai_api_key = os.environ.get("OPENAI_API_KEY")
    llm = OpenAI(api_key = openai.api_key , model="text-davinci-003", temperature=0.8, max_tokens=150)
    return llm

def setup_financial_chains(llm, level):
    fin_routes = [
        {
            "name": "InvestmentAdvisor",
            "description": "Route for clients with a debt ratio less than 0.3.",
            "prompt_template": investment_template
        },
        {
            "name": "DebtAdvisor",
            "description": "Route for clients with a debt ratio of 0.3 or higher.",
            "prompt_template": debt_template
        },
    ]

    destination_chains = {}
    for p_info in fin_routes:
        prompt = PromptTemplate(template=p_info["prompt_template"], input_variables=["input"])
        chain = LLMChain(llm=llm, prompt=prompt)
        destination_chains[p_info["name"]] = chain

    financial_prompt = """
    Hello! As your financial chatbot, I'm here to help you understand your current financial situation. 
    Based on your financial knowledge, which you've indicated as {level}, I'll tailor my explanation to suit your understanding.

    Now, let's summarize your financial status.
    """

    MULTI_PROMPT_ROUTER_TEMPLATE = """\
Given a raw text input to a language model select the model prompt best suited for \
the input. You will be given the names of the available prompts and a description of \
what the prompt is best suited for. You may also revise the original input if you \
think that revising it will ultimately lead to a better response from the language \
model.

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{{{
    "destination": string \ name of the prompt to use or "DEFAULT"
    "next_inputs": string \ a modified version of the original input. It is modified to contai only: the "savings" value, the "debt" value, the "income" value, and the "summary" provided above.
}}}}
```

REMEMBER: "destination" MUST be one of the candidate prompt names specified below OR \
it can be "DEFAULT" if the input is not well suited for any of the candidate prompts.
REMEMBER: "next_inputs" is not the original input. It is modified to contain: the "savings" value, the "debt" value, the "income" value, and the "summary" provided above.

<< CANDIDATE PROMPTS >>
{destinations}

<< INPUT >>
{{input}}

<< OUTPUT (must include ```json at the start of the response) >>
<< OUTPUT (must end with ```) >>
    """

    prompt = financial_prompt + MULTI_PROMPT_ROUTER_TEMPLATE
    destinations = [f"{route['name']}: {route['description']}" for route in fin_routes]
    destinations_str = "\n".join(destinations)
    router_template = prompt.format(destinations=destinations_str, level=level)

    router_prompt = PromptTemplate(
        template=router_template,
        input_variables=["input"],
        output_parser=RouterOutputParser(),
    )
    router_chain = LLMRouterChain.from_llm(llm, router_prompt)

    return MultiPromptChain(
        router_chain=router_chain,
        destination_chains=destination_chains,
        default_chain=ConversationChain(llm=llm, output_key="text"),
        verbose=False,
    )



def loadCSVFile(csv_file):
  # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
        # Copy the contents of the uploaded file to the temporary file
        shutil.copyfileobj(uploaded_file, tmp_file)
        tmp_file_path = tmp_file.name

    # Now you can use the file path with CSVLoader
    loader = CSVLoader(tmp_file_path)
    data = loader.load()
    text = data[0]['page_content']
    
    # Optionally delete the temporary file if no longer needed
    # os.remove(tmp_file_path)


 
def run10times(csv_file, chain):
    final_result = ""
    #for _ in range(10):
    result = chain.run(csv_file)
    #final_result += result + "\n"
    return result

def process_financial_data(text,level):
    # Split the text by comma and strip whitespace and dollar signs
    values = [v.strip().replace('$', '').replace(',', '') for v in text.split(',')]

    # Initialize default values
    total_savings = "0"
    monthly_debt = "0"
    monthly_income = "0"

    # Assign values based on the input text
    try:
        if len(values) > 0:
            total_savings = float(values[0])
        if len(values) > 1:
            monthly_debt = float(values[1])
        if len(values) > 2:
            monthly_income = float(values[2])
    except ValueError as e:
        st.error(f"Error processing financial data: {e}")
        return None, None, None

    return total_savings, monthly_debt, monthly_income

def main():
    st.header("Welcome to FiniBot Financial Advisory! Please upload your financial spreadsheet.")

    level = st.radio("Select your experience level:", ("Novice", "Expert"))
    uploaded_file = st.file_uploader("Upload your financial spreadsheet", type=['csv'])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)  # Adjust this line if your spreadsheet is in a different format
        st.dataframe(df)  # Displaying the spreadsheet

       # text = loadCSVFile(uploaded_file)

# Initialize an empty string to store text
        text = ""

# Iterate over rows
        for index, row in df.iterrows():
    # For each row, concatenate column values to the text string
             row_text = ', '.join(str(value) for value in row)
             text += row_text + '\n'  # Add a newline character to separate rows


        st.markdown(text)

       


        total_savings, monthly_debt, monthly_income = process_financial_data(text, level)

        llm = get_llm()
        financial_chain = setup_financial_chains(llm, level)
        result = run10times(text, financial_chain)

       

        st.markdown("### Financial Summary")
        st.markdown(f"- Total savings: ${total_savings}")
        st.markdown(f"- Monthly debt: ${monthly_debt}")
        st.markdown(f"- Monthly income: ${monthly_income}\n")

        st.markdown("### Financial situation:")
        st.markdown(f"  Financial level: {level}\n")

        st.markdown("### Recommendation:")
        st.markdown(result)

if __name__ == "__main__":
    main()

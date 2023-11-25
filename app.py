import streamlit as st
import os
import pandas as pd
from io import StringIO
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain, LLMChain
from langchain.chains.router import MultiPromptChain, LLMRouterChain
from langchain.chains.router.llm_router import RouterOutputParser

# Define your investment and debt templates (placeholders here)
investment_template = "..."  # Replace with your actual investment template
debt_template = "..."  # Replace with your actual debt template

def get_llm():
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    llm = OpenAI(api_key=openai_api_key, model="text-davinci-003", temperature=0.8, max_tokens=150)
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

    MULTI_PROMPT_ROUTER_TEMPLATE = """
    ...  # Your MULTI_PROMPT_ROUTER_TEMPLATE content
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

def loadCSVFile(uploaded_file):
    text_io = StringIO(uploaded_file.getvalue().decode("utf-8"))
    df = pd.read_csv(text_io)
    text = df.to_string(index=False)
    return text

def run10times(csv_file, chain):
    final_result = ""
    for _ in range(10):
        result = chain.run(csv_file)
        final_result += result + "\n"
    return final_result

def process_financial_data(text, level):
    for line in text.split('\n'):
        if 'savings:' in line:
            total_savings = line.split(':')[1].strip().replace('$', '').replace(',', '')
        elif 'credit card debt:' in line:
            monthly_debt = line.split(':')[1].strip().replace('$', '').replace(',', '')
        elif 'income:' in line:
            monthly_income = line.split(':')[1].strip().replace('$', '').replace(',', '')

    total_savings = float(total_savings)
    monthly_debt = float(monthly_debt)
    monthly_income = float(monthly_income)

    return total_savings, monthly_debt, monthly_income

def main():
    st.header("Welcome to FiniBot Financial Advisory! Please upload your financial spreadsheet.")

    level = st.radio("Select your experience level:", ("Novice", "Expert"))
    uploaded_file = st.file_uploader("Upload your financial spreadsheet", type=['csv'])

    if uploaded_file is not None:
        text = loadCSVFile(uploaded_file)
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

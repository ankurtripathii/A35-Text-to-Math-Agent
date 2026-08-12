import streamlit as st

from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain_community.tools import Tool
import numexpr

def calculator(expression):
    try:
        result = numexpr.evaluate(expression)
        return str(result)
    except Exception as e:
        return f"Calculation Error: {e}"
math_tool = Tool(name="Calculator",func=calculator,description="Useful for solving mathematical expressions.")

llm = ChatOllama(model="llama3.2",temperature=0)
agent = initialize_agent(tools=[math_tool],llm=llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True)

st.title("Text-to-Math Agent")
if "history" not in st.session_state:
    st.session_state.history = []
question = st.text_input("Enter your math problem")

if st.button("Solve"):
    prompt = f"""Solve the following math problem step by stepProblem:{question}Use the calculator tool whenever calculations are required"""
    answer = agent.run(prompt)
    st.session_state.history.append({"question": question,"answer": answer})

st.divider()
st.header("Conversation History")
for chat in st.session_state.history:
    st.write("**Question:**", chat["question"])
    st.write("**Answer:**", chat["answer"])
    st.write("---")
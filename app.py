import re
import numexpr
import streamlit as st
from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import Tool

def calculator(expression):
    expression = expression.strip()
    expression = re.sub(r'(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)',
                         r'(\1 / 100) * \2', expression, flags=re.IGNORECASE)
    expression = expression.replace('%', '/100')
    return str(numexpr.evaluate(expression))

math_tool = Tool(
    name="Calculator",
    func=calculator,
    description=("Use this tool for arithmetic. Give it a mathematical expression. "
                 "It supports decimals and simple percentage expressions such as 15% of 240.")
)

@st.cache_resource
def get_agent():
    llm = ChatOllama(model="llama3.2", temperature=0)
    return initialize_agent(
        tools=[math_tool], llm=llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True, max_iterations=8, handle_parsing_errors=True,
        early_stopping_method="generate",
      
    )

agent = get_agent()

def solve_math(question, previous_context=""):
    if previous_context:
        prompt = (f"Previous context:\n{previous_context}\n\n"
                   f"New problem:\n{question}\n"
                   "Use the Calculator tool for arithmetic and give the final answer.")
    else:
        prompt = question + "\nUse the Calculator tool for arithmetic and give the final answer."
    return agent.run(prompt)



def clean_answer(answer):                     # <-- new, goes right after solve_math
    return answer.replace("$", "").strip()


st.set_page_config(page_title="Text-to-Math Agent")
st.title("Text-to-Math Agent")

if "history" not in st.session_state:
    st.session_state.history = []

question = st.text_input("Enter your math problem", placeholder="Example: What is 15% of 800?")


if st.button("Solve", type="primary"):
    if not question.strip():
        st.warning("Please enter a mathematical question.")
    else:
        # build context from the last exchange so the agent, not just the UI, sees it
        previous_context = ""
        if st.session_state.history:
            last = st.session_state.history[-1]
            previous_context = f"Q: {last['question']}\nA: {last['answer']}"

        with st.spinner("Thinking..."):
            answer = solve_math(question, previous_context)

        answer = clean_answer(answer)
        st.success("Solved!")
        st.write(f"**Answer:** {answer}")
        st.session_state.history.append({"question": question, "answer": answer})

st.divider()
st.header("Conversation History")
if not st.session_state.history:
    st.info("No conversation yet.")
else:
    for chat in st.session_state.history:
        st.write(f"**Q:** {chat['question']}")
        st.write(f"**A:** {chat['answer']}")
        st.divider()
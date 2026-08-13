import re
import numexpr
import streamlit as st

from langchain_community.tools import Tool

def calculator(expression):
    """
    Deterministic calculator.

    Supports:
    - percentages
    - decimals
    - normal arithmetic
    """

    try:

        if isinstance(expression, dict):
            expression = (
                expression.get("expression")
                or expression.get("__arg1")
                or expression.get("input")
                or ""
            )

        expression = str(expression).strip()

        # Remove common natural-language prefixes
        expression = re.sub(
            r"^(what is|calculate|solve|find|compute)\s+",
            "",
            expression,
            flags=re.IGNORECASE
        )

        expression = expression.replace("?", "").strip()


        match = re.search(
            r"(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)",
            expression,
            re.IGNORECASE
        )

        if match:

            percentage = float(match.group(1))
            number = float(match.group(2))

            result = (percentage / 100) * number

            return str(result)


        expression = re.sub(
            r"(\d+(?:\.\d+)?)\s*%",
            r"(\1/100)",
            expression
        )



        result = numexpr.evaluate(expression)

        return str(result)

    except Exception as e:

        return f"Calculation Error: {e}"




math_tool = Tool(
    name="Calculator",
    func=calculator,
    description="""
    Mathematical calculator.

    Supports:
    - percentages
    - decimal calculations
    - addition
    - subtraction
    - multiplication
    - division

    Examples:
    15% of 100
    15% of 800
    15.5 * 3
    100 + 50
    """
)

st.set_page_config(
    page_title="Text-to-Math Agent",
)

st.title("Text-to-Math Agent")

st.write(
    "Ask a mathematical question and the Calculator tool "
    "will provide the exact result."
)




if "history" not in st.session_state:
    st.session_state.history = []




question = st.text_input(
    "Enter your math problem",
    placeholder="Example: What is 15% of 800?"
)




if st.button("Solve", type="primary"):

    if not question.strip():

        st.warning("Please enter a mathematical question.")

    else:

        with st.spinner("Calculating..."):

            result = math_tool.invoke(question)



        if str(result).startswith("Calculation Error"):

            st.error(result)

            answer = result

        else:

            answer = f"**Answer: {result}**"

            st.success("Solved!")

            st.write(answer)

        st.session_state.history.append(
            {
                "question": question,
                "answer": answer
            }
        )

st.divider()

st.header("Conversation History")


if not st.session_state.history:

    st.info("No conversation yet.")

else:

    for chat in st.session_state.history:

        st.write("**Question:**")
        st.write(chat["question"])

        st.write("**Answer:**")
        st.write(chat["answer"])

        st.divider()
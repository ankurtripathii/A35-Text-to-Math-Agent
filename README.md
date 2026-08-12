# Assignment 35 - Text-to-Math Agent

I built this project to be a Text-to-Math Problem Solver built using LangChain, Ollama, and Streamlit.

It also uses Streamlit Session State to save previous questions and answers during the session.

Technologies Used

* Python
* LangChain
* Ollama (Llama 3.2)
* Streamlit
* NumExpr

Installation

Install the required packages using this command

pip install -r requirements.txt

Run the Project

Start the Ollama model:

ollama run llama3.2

Run the Streamlit application:

python -m streamlit run app.py

## Example Questions

* Ravi has 25 apples. He buys 15 more and gives away 10. How many apples remain?
* Find 15% of 800.
* Solve: 2x + 6 = 18


from langchain import PromptTemplate

DEFAULT_TEMPLATE = """
Current conversation:
{chat_history}

Context:
{context}

Question: {question}
Helpful Answer:
"""

PROMPT = PromptTemplate(input_variables=['chat_history', 'question', 'context'], template=DEFAULT_TEMPLATE)

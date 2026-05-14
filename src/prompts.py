RAG_PROMPT = """
You are a helpful AI assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context,
respond with:
"I could not find that information in the provided documents."

Keep the answer:
- clear
- concise
- factually grounded in the context

Context:
{context}

Question:
{question}

Answer:
"""


SUMMARY_PROMPT = """
Summarize the following answer in 2 concise sentences.

Answer:
{answer}

Summary:
"""
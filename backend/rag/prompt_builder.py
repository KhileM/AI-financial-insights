import os

def build_prompt(user_query, context_chunks):
    """
    This function takes the user's query and a list of relevant text chunks (retrieved from a vector store - ChromaDB),
    formats them into a readable and structured prompt, and returns the full string to be used in an LLM call.

    Args:
        user_query (str): The question or query from the user.
        context_chunks (List[str]): A list of relevant text chunks to provide context to the LLM.

    Returns:
        str: A formatted prompt string combining the assistant's role, context, the user's question, and space for the answer.
    """
    # Join all relevant chunks using a separator to make them easier to distinguish
    context_text = "\n---\n".join(context_chunks)

    # Return a structured prompt with role, context, and question
    return f"""You are a data analyst assistant.

Context:
{context_text}

Question: {user_query}
Answer:"""
"""
RAG Prompt Design

- System prompt restricts answers to retrieved documents.
- Context contains retrieved chunks with source labels.
- Conversation history maintains chat continuity.
- User query is separated for clarity.
- Context length is capped to reduce prompt size.
"""

MAX_CONTEXT_CHARS = 6000

NOT_FOUND_INSTRUCTION = (
    "If the provided context does not contain enough information "
    "to answer the question, respond with exactly: "
    '"I could not find information about that in the uploaded documents."'
)

SYSTEM_PROMPT = (
    "You are a document assistant. Answer the user's question using ONLY "
    "the context provided below from uploaded documents. "
    "Do not use outside knowledge or guess. "
    "If the context is insufficient, say you could not find the information "
    "in the uploaded documents. "
    "Keep answers concise and factual."
)


def format_context_block(chunks):

    context = ""

    for chunk in chunks:

        label = (
            f"[{chunk['source_file']} | chunk {chunk['chunk_id']}]"
        )

        candidate = (
            f"{label}\n"
            f"{chunk['text']}\n\n"
        )

        if len(context) + len(candidate) > MAX_CONTEXT_CHARS:
            break

        context += candidate

    return context.strip()


def build_rag_messages(
    query,
    chunks,
    history_text
):

    context = format_context_block(
        chunks
    )

    user_content = (
            f"[CONTEXT]\n"
            f"{context}\n\n"

            f"[HISTORY]\n"
            f"{history_text}\n\n"

            f"[QUERY]\n"
            f"{query}\n\n"

            f"{NOT_FOUND_INSTRUCTION}"
        )

    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_content
        }
    ]

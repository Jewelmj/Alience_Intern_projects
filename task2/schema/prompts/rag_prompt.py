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


def format_context_block(
    chunks
):

    sections = []

    for chunk in chunks:

        label = (
            f"[{chunk['source_file']} | chunk {chunk['chunk_id']}]"
        )

        sections.append(
            f"{label}\n{chunk['text']}"
        )

    return "\n\n".join(sections)


def build_rag_messages(
    query,
    chunks
):

    context = format_context_block(
        chunks
    )

    user_content = (
        f"Context from uploaded documents:\n\n"
        f"{context}\n\n"
        f"Question: {query}\n\n"
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

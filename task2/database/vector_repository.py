from database.vector_store import (
    collection
)

def save_embeddings(embedding_records):

    ids = []
    embeddings = []
    documents = []
    metadatas = []

    for record in embedding_records:

        ids.append(
            f"{record['session_id']}_{record['source_file']}_{record['chunk_id']}"
        )

        embeddings.append(
            record["embedding"]
        )

        documents.append(
            record["text"]
        )

        metadata = record.copy()

        metadata.pop("embedding", None)
        metadata.pop("text", None)
        metadata.pop("vector_dimension", None)

        metadatas.append(metadata)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )


def search_similar(query_embedding, session_id, top_k=5):
    return collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k,
        where={
            "session_id": session_id
        }
    )

def delete_document_embeddings(
    source_file
):

    results = collection.get(
        where={
            "source_file": source_file
        }
    )

    ids = results.get(
        "ids",
        []
    )

    if ids:

        collection.delete(
            ids=ids
        )

    return len(ids)
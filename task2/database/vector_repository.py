from database.vector_store import (
    collection
)

def save_embeddings(
    embedding_records
):

    ids = []
    embeddings = []
    documents = []
    metadatas = []

    for record in embedding_records:

        ids.append(
            f"{record['source_file']}_{record['chunk_id']}"
        )

        embeddings.append(
            record["embedding"]
        )

        documents.append(
            record["text"]
        )

        metadatas.append(
            {
                "source_file":
                    record["source_file"],

                "chunk_id":
                    record["chunk_id"],

                "chunk_length":
                    record["chunk_length"]
            }
        )

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )


def search_similar(
    query_embedding,
    top_k=5
):

    return collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k
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
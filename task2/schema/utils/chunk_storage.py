import json
from pathlib import Path

CHUNK_FOLDER = Path(
    "storage/chunks"
)


def save_chunk_metadata(
    filename,
    chunks
):

    metadata = []

    for idx, chunk in enumerate(chunks):

        metadata.append(
            {
                "chunk_id": idx,
                "source_file": filename,
                "chunk_length": len(chunk),
                "text": chunk
            }
        )

    output_file = (
        CHUNK_FOLDER
        / f"{Path(filename).stem}_chunks.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4,
            ensure_ascii=False
        )

    return metadata, output_file.name
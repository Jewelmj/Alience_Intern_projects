import json
from pathlib import Path

VECTOR_FOLDER = Path(
    "storage/vectors"
)


def save_vectors(
    filename,
    embedding_records
):

    output_file = (
        VECTOR_FOLDER
        / f"{Path(filename).stem}_vectors.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            embedding_records,
            f,
            indent=4,
            ensure_ascii=False
        )

    return output_file.name
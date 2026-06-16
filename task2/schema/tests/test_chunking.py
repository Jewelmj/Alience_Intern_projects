import json

from schema.utils.text_chunking import (
    chunk_text
)
from pathlib import Path
from schema.utils.chunk_storage import (
    save_chunk_metadata
)

def test_chunk_creation():

    text = "Hello " * 1000

    chunks = chunk_text(text)

    assert len(chunks) > 1
    assert all(
        len(chunk) > 0
        for chunk in chunks
    )

def test_chunk_order():

    text = (
        "FIRST " * 1000 +
        "SECOND " * 1000
    )

    chunks = chunk_text(text)

    combined = "".join(chunks)

    assert combined.index("FIRST") < combined.index("SECOND")

def test_chunk_metadata_saved():

    chunks = [
        "chunk one",
        "chunk two"
    ]

    metadata, filename = save_chunk_metadata(
        "sample.pdf",
        chunks
    )

    output_file = (
        Path("storage/chunks")
        / filename
    )

    try:

        assert output_file.exists()

        with open(output_file) as f:
            data = json.load(f)

        assert len(data) == 2
        assert data[0]["chunk_id"] == 0
        assert data[1]["chunk_id"] == 1
        assert data[0]["source_file"] == "sample.pdf"
        assert data[0]["text"] == "chunk one"
        assert data[0]["chunk_length"] == len("chunk one")

        assert data[1]["source_file"] == "sample.pdf"
        assert data[1]["text"] == "chunk two"
        assert data[1]["chunk_length"] == len("chunk two")

    finally:

        output_file.unlink(
            missing_ok=True
        )


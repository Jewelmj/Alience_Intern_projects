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

    filename = save_chunk_metadata(
        "sample.pdf",
        chunks
    )

    output_file = (
        Path("storage/chunks")
        / filename
    )

    assert output_file.exists()
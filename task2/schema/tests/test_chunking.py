from schema.utils.text_chunking import (
    chunk_text
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
from schema.utils.text_chunking import chunk_text
from schema.utils.chunk_storage import save_chunk_metadata

text = "Hello World " * 1000

chunks = chunk_text(text)

filename = save_chunk_metadata(
    "sample.pdf",
    chunks
)

print("Saved:", filename)
print("Chunks:", len(chunks))
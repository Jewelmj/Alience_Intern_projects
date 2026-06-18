from agents.embedding.agent import EmbeddingAgent
from agents.extraction.agent import ExtractionAgent
from agents.ingestion.agent import IngestionAgent
from agents.retrieval.agent import RetrievalAgent

embedding_agent = EmbeddingAgent()

extraction_agent = ExtractionAgent()

ingestion_agent = IngestionAgent(
    extraction_agent,
    embedding_agent
)

retrieval_agent = RetrievalAgent(
    embedding_agent
)
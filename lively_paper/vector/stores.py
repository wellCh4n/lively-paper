from langchain.vectorstores import VectorStore, ClickhouseSettings

from lively_paper.model.embeddings import m3e
from lively_paper.vector.clickhouse import Clickhouse

# vectorStore: VectorStore = Chroma(embedding_function=m3e, persist_directory='/Users/wellch4n/chroma')

settings = ClickhouseSettings()
vector_store: VectorStore = Clickhouse(embedding=m3e, config=settings)

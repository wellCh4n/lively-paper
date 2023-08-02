from langchain.vectorstores import VectorStore, Chroma, Clickhouse, ClickhouseSettings

from lively_paper.model.embeddings import m3e


class Stores(object):
    def __init__(self) -> None:
        super().__init__()


# vectorStore: VectorStore = Chroma(embedding_function=m3e, persist_directory='/Users/wellch4n/chroma')

settings = ClickhouseSettings()
vectorStore: VectorStore = Clickhouse(embedding=m3e, config=settings)

from langchain.embeddings import SentenceTransformerEmbeddings, HuggingFaceEmbeddings


class Embeddings(object):
    def __init__(self) -> None:
        super().__init__()


m3e: HuggingFaceEmbeddings = SentenceTransformerEmbeddings(model_name='moka-ai/m3e-base')

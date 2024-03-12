from qdrant_client import QdrantClient
import os
from qdrant_client.http import models
from langchain.vectorstores import Qdrant
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain import OpenAI
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from langchain.document_loaders import (
    PyMuPDFLoader,
)

load_dotenv()
client = QdrantClient(
    url=os.getenv("QDRANT_HOST"),
    api_key=os.getenv("QDRANT_API_KEY"),
    timeout=100000,
)


# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
embeddings = OpenAIEmbeddings()
vectorStore = Qdrant(
    client=client,
    collection_name=os.getenv("QDRANT_COLLECTION_ISLAMIC"),
    embeddings=embeddings,
)
retriever = vectorStore.as_retriever(search_kwargs={"k": 10})

text_splitter = RecursiveCharacterTextSplitter(
    separators=[
        ".",
        "\n",
        "\t",
        "\r",
        "\f",
        "\v",
        "\0",
        "\x0b",
        "\x0c",
        "\n\n",
        "\n\n\n",
    ],
    chunk_size=1000,
    chunk_overlap=200,
)
# 1536 open ai embeddings
# 768 hugging face embeddings
# vectors_config = models.VectorParams(size=1536, distance=models.Distance.COSINE)
# client.recreate_collection(
#     collection_name=os.getenv("QDRANT_COLLECTION_ISLAMIC"),
#     vectors_config=vectors_config,
# )
# print("collection created")
loader = PyMuPDFLoader(
    "D:/projects/AI projects/privateGPT-main/source_documents/al_mizan_01.pdf"
)
print("loaders created")
docs = loader.load_and_split(text_splitter=text_splitter)
print("docs loaded")
vectorStore.add_documents(docs)
print("docs added")

import os
from pprint import pprint

from langchain_community.vectorstores import Milvus
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
connection_args = {"host": os.environ.get("URL", "localhost"), "port": "19530"}


doc_vector_store = Milvus(
    embedding_function=embeddings,
    connection_args=connection_args,
    collection_name="tables",
)

query = "What are the columns in the Customers table?"
docs = doc_vector_store.similarity_search(query, k=20)
pprint(docs)

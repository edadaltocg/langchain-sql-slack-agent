import os
from pathlib import Path

import pandas as pd
from langchain_community.vectorstores import Milvus
from langchain_core.documents import Document
from tqdm import tqdm
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
connection_args = {"host": os.environ.get("URL", "localhost"), "port": "19530"}


if __name__ == "__main__":
    docs = []
    encodings = pd.read_csv("data_v2/encodings_with_embeddings_0_1_0.csv")
    for _, row in encodings.iterrows():
        table_name = row["table"]
        metadata = {"table": table_name}
        content = f"""Table: {row['table']}, \
Table Description: {row['table_description']}, \
Column: {row['column']}, \
Column Description: {row['column_description']}"""
        docs.append(Document(metadata=metadata, page_content=content))
    assert len(docs) > 0, "No documents found in the encodings file"

    people = []
    path = Path("../fake-db-gen/data/people/people.csv")
    df = pd.read_csv(path)
    for row in df.iterrows():
        row = row[1]
        metadata = {
            "tables_created": row["Tables Created"],
        }
        content = f"""name: @{row["Name"]}, seniority: {row["Seniority"]}, tables created: {row["Tables Created"]}, \
job description: {row['Job Description']}"""
        doc = Document(metadata=metadata, page_content=content)
        people.append(doc)

    slack_chat = []
    chat = pd.read_csv("data_v2/slack_fake_data/threads.csv")
    for thread_ts, group in chat.groupby("thread_ts"):
        metadata = {"thread_ts": thread_ts}
        content = f"{group['username']}: {group['message']}"
        doc = Document(metadata=metadata, page_content=content)
        slack_chat.append(doc)

    doc_vector_store = Milvus(
        embedding_function=embeddings,
        connection_args=connection_args,
        collection_name="tables_0_1_0",
        drop_old=True,
    ).from_documents(
        docs,
        embedding=embeddings,
        connection_args=connection_args,
        collection_name="tables_0_1_0",
    )

    people_vector_store = Milvus(
        embedding_function=embeddings,
        connection_args=connection_args,
        collection_name="people_0_1_0",
        drop_old=True,
    ).from_documents(
        people,
        embedding=embeddings,
        connection_args=connection_args,
        collection_name="people_0_1_0",
    )

    slack_vector_store = Milvus(
        embedding_function=embeddings,
        connection_args=connection_args,
        collection_name="slack_0_1_0",
        drop_old=True,
    ).from_documents(
        slack_chat,
        embedding=embeddings,
        connection_args=connection_args,
        collection_name="slack_0_1_0",
    )

    query = "What are the columns in the Customers table?"
    docs = doc_vector_store.similarity_search(query)
    print(docs)

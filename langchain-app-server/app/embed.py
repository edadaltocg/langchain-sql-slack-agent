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
    schema_path = Path("../fake-db-gen/data/schema")
    for file in tqdm(os.listdir(schema_path)):
        if file.endswith(".csv"):
            df = pd.read_csv(schema_path / file)
            for row in df.iterrows():
                row = row[1]
                filename = file.split(".")[0]
                metadata = {"table": filename}
                content = f"""table: `{filename}`, column: `{row["column"]}`, description: {row["description"]}"""
                docs.append(Document(metadata=metadata, page_content=content))

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

    doc_vector_store = Milvus(
        embedding_function=embeddings,
        connection_args=connection_args,
        collection_name="tables",
        drop_old=True,
    ).from_documents(
        docs,
        embedding=embeddings,
        connection_args=connection_args,
        collection_name="tables",
    )

    people_vector_store = Milvus(
        embedding_function=embeddings,
        connection_args=connection_args,
        collection_name="people",
        drop_old=True,
    ).from_documents(
        people,
        embedding=embeddings,
        connection_args=connection_args,
        collection_name="people",
    )

    query = "What are the columns in the Customers table?"
    docs = doc_vector_store.similarity_search(query)
    print(docs)
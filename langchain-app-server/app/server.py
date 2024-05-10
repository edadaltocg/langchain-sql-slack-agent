import os
from pathlib import Path
from typing import List, Union
from langchain_core.pydantic_v1 import BaseModel, Field

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.vectorstores import Milvus
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langserve import add_routes
from tqdm import tqdm

from langchain.schema import SystemMessage, HumanMessage, AIMessage
from app.chains.rag_qa import make_conversational_rag_chain

print("Starting server")
app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

query_model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=1)
# model_id = "gpt-3.5-turbo"
model_id = "gpt-4-turbo-2024-04-09"
response_model = ChatOpenAI(model=model_id, temperature=1)

system_prompt_template = """You are a helpful assistant who answers questions about tabular data. Your name is Carl."""
response_prompt_template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum. Tell me all relevant columns with their description and all relevant tables to look.
Tag with @<person name> one or two relevant people if necessary who might know the answer.

Context:
{context}

People:
{people}

Question: {question}
Helpful Answer:"""


messages = [
    SystemMessagePromptTemplate.from_template(system_prompt_template),
    HumanMessagePromptTemplate.from_template(response_prompt_template),
    MessagesPlaceholder("chat_history"),
]
rag_prompt = ChatPromptTemplate.from_messages(messages)
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
connection_args = {"host": "127.0.0.1", "port": "19530"}


@chain
def docs_to_str(docs: list[Document]):
    out = ""
    for doc in docs:
        out += f"""table: `{doc.metadata['table']}`, \
        column: `{doc.metadata['column']}`, \
        description: \"{doc.page_content}\"\n"""
    return out


@chain
def people_to_str(people: list[Document]):
    out = ""
    for doc in people:
        out += f"name: `{doc.metadata['name']}`, \
        seniority: `{doc.metadata['seniority']}`, \
        {doc.page_content} \n"
    return out


type_dict = {
    "int": "integer",
}


def build_metadata_field_attribute(name, description, t):
    return AttributeInfo(
        name=name,
        description=description,
        type=t,
    )


def build_document(metadata, content):
    return Document(metadata=metadata, page_content=content)


docs = []
docs_field_metadata = [
    AttributeInfo(name="table", description="The name of the table", type="string"),
    AttributeInfo(name="column", description="The name of the column", type="string"),
]
schema_path = Path("../fake-db-gen/data/schema")
metadata_field_info = []
for file in tqdm(os.listdir(schema_path)):
    if file.endswith(".csv"):
        df = pd.read_csv(schema_path / file)
        for row in df.iterrows():
            row = row[1]
            filename = file.split(".")[0]
            metadata = {"table": filename, "column": row["column"]}
            docs.append(
                build_document(
                    metadata, f"Table: {filename}, Column: {row['column']}, Description: {row['description']}"
                )
            )


people = []
people_field_metadata = [
    AttributeInfo(name="name", description="The name of the person", type="string"),
    AttributeInfo(name="seniority", description="The seniority of the person", type="string"),
    AttributeInfo(name="tables_created", description="The names of the tables the person has created", type="string"),
]
path = Path("../fake-db-gen/data/people/people.csv")
df = pd.read_csv(path)
for row in df.iterrows():
    row = row[1]
    # Tables Created,Job Description,Online Now
    metadata = {
        "name": row["Name"],
        "seniority": row["Seniority"],
        "tables_created": row["Tables Created"],
    }
    content = f"Tables Created: {row['Tables Created']}, Job Description: {row['Job Description']}"
    doc = Document(metadata=metadata, page_content=content)
    people.append(doc)

doc_vector_store = Milvus.from_documents(
    docs,
    embedding=embeddings,
    connection_args=connection_args,
    collection_name="tables",
    drop_old=True,
)

people_vector_store = Milvus.from_documents(
    people,
    embedding=embeddings,
    connection_args=connection_args,
    collection_name="people",
    drop_old=True,
)

document_content_description = "Description of a column in a table"
docs_retriever = SelfQueryRetriever.from_llm(
    query_model,
    doc_vector_store,
    document_content_description,
    metadata_field_info,
    verbose=True,
    enable_limit=True,
    # search_kwargs={"k": 20},
    search_kwargs={"score_threshold": 0.5},
)

people_content_description = "Tables created and job description of a data person"
people_retriever = SelfQueryRetriever.from_llm(
    query_model,
    people_vector_store,
    people_content_description,
    people_field_metadata,
    verbose=True,
    enable_limit=True,
    search_kwargs={"score_threshold": 0.8},
)

rerank_model = ...  # TODO:


rag_chain = (
    {
        "context": docs_retriever | docs_to_str,
        "people": people_retriever | people_to_str,
    }
    | rag_prompt
    | response_model
)  # | StrOutputParser()

conversational_rag_chain = make_conversational_rag_chain(docs_retriever, people_retriever, docs_to_str, people_to_str)

print(conversational_rag_chain.invoke({"input": "What is the description of the column age?", "session_id": "123"}))
print(conversational_rag_chain.invoke({"input": "Say the name of the column in caps", "session_id": "123"}))


####################################################
# class InputChat(BaseModel):
#     """Input for the chat endpoint."""
#
#     messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
#         ...,
#         description="The chat messages representing the current conversation.",
#     )
#


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


add_routes(
    app,
    rag_chain,
    path="/rag",
)


add_routes(
    app,
    conversational_rag_chain,
    path="/rag-conversational",
    playground_type="default",
)


add_routes(
    app,
    ChatOpenAI(),
    path="/openai",
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)

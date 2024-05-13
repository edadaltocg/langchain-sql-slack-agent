import os

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
from app.embed import embeddings, connection_args

from langchain.schema import SystemMessage, HumanMessage, AIMessage
from app.chains.rag_qa import make_conversational_rag_chain, InputDict
from app.chains.chat import ChatRequest, chain as chat_chain

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

temperature = 0
query_model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=temperature)
# model_id = "gpt-3.5-turbo"
model_id = "gpt-4-turbo-2024-04-09"
response_model = ChatOpenAI(model=model_id, temperature=temperature)

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


@chain
def docs_to_str(docs: list[Document]):
    out = ""
    for doc in docs:
        out += f"{doc.page_content}\n"
    return out


@chain
def people_to_str(people: list[Document]):
    out = ""
    for doc in people:
        out += f"{doc.page_content}\n"
    return out


docs_field_metadata = [
    AttributeInfo(name="table", description="The name of the table", type="string"),
    # AttributeInfo(name="column", description="The name of the column", type="string"),
]

people_field_metadata = [
    # AttributeInfo(name="name", description="The name of the person", type="string"),
    # AttributeInfo(name="seniority", description="The seniority of the person", type="string"),
    AttributeInfo(name="tables_created", description="The names of the tables the person has created", type="string"),
]

doc_vector_store = Milvus(
    embedding_function=embeddings,
    connection_args=connection_args,
    collection_name="tables",
)

people_vector_store = Milvus(
    embedding_function=embeddings,
    connection_args=connection_args,
    collection_name="people",
)

document_content_description = "Description of a column in a table"
docs_retriever = SelfQueryRetriever.from_llm(
    query_model,
    doc_vector_store,
    document_content_description,
    docs_field_metadata,
    verbose=True,
    enable_limit=True,
    search_kwargs={"k": 25},
    # search_kwargs={"score_threshold": 0.45},
)
docs_retriever = doc_vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 25, "score_threshold": 0.25},
)

people_content_description = "Tables created and job description of a data person"
people_retriever = SelfQueryRetriever.from_llm(
    query_model,
    people_vector_store,
    people_content_description,
    people_field_metadata,
    verbose=True,
    enable_limit=True,
    search_kwargs={"k": 1},
    # search_kwargs={"score_threshold": 0.45},
)
people_retriever = people_vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 1, "score_threshold": 0.25},
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

# print(conversational_rag_chain.invoke({"question": "What is the description of the column age?", "session_id": "123"}))
# print(conversational_rag_chain.invoke({"question": "Say the name of the column in caps", "session_id": "123"}))


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
    # playground_type="chat",
    input_type=InputDict,
)


add_routes(
    app,
    ChatOpenAI(),
    path="/openai",
)

add_routes(
    app,
    chat_chain,
    path="/chat",
    playground_type="chat",
    input_type=ChatRequest,
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

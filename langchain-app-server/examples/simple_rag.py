from langchain.chains.query_constructor.base import AttributeInfo
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.vectorstores import Milvus
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAI, OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
docs = [
    Document(
        page_content="A bunch of scientists bring back dinosaurs and mayhem breaks loose",
        metadata={"year": 1993, "rating": 7.7, "genre": "action"},
    ),
    Document(
        page_content="Leo DiCaprio gets lost in a dream within a dream within a dream within a ...",
        metadata={"year": 2010, "genre": "thriller", "rating": 8.2},
    ),
    Document(
        page_content="A bunch of normal-sized women are supremely wholesome and some men pine after them",
        metadata={"year": 2019, "rating": 8.3, "genre": "drama"},
    ),
    Document(
        page_content="Three men walk into the Zone, three men walk out of the Zone",
        metadata={"year": 1979, "rating": 9.9, "genre": "science fiction"},
    ),
    Document(
        page_content="A psychologist / detective gets lost in a series of dreams within dreams within dreams and Inception reused the idea",
        metadata={"year": 2006, "genre": "thriller", "rating": 9.0},
    ),
    Document(
        page_content="Toys come alive and have a blast doing so",
        metadata={"year": 1995, "genre": "animated", "rating": 9.3},
    ),
]

connection_args = {"host": "127.0.0.1", "port": "19530"}
# vector_store = Milvus.from_documents(
#     docs,
#     embedding=embeddings,
#     connection_args=connection_args,
# )
vector_store = Milvus(
    embedding_function=embeddings,
    connection_args=connection_args,
)


metadata_field_info = [
    AttributeInfo(
        name="genre",
        description="The genre of the movie",
        type="string",
    ),
    AttributeInfo(
        name="year",
        description="The year the movie was released",
        type="integer",
    ),
    AttributeInfo(name="rating", description="A 1-10 rating for the movie", type="float"),
]

document_content_description = "Brief summary of a movie"
llm = OpenAI(temperature=0)
retriever = SelfQueryRetriever.from_llm(
    llm,
    vector_store,
    document_content_description,
    metadata_field_info,
    verbose=True,
    enable_limit=True,
)


# This example only specifies a relevant query
# print(retriever.invoke("What are some movies about dinosaurs"))

# This example specifies a filter
# print(retriever.invoke("What are some highly rated movies (above 9)?"))


# context compressor
# documents to strings
def doc_to_str(docs: list[Document]):
    for doc in docs:
        yield f"metadata: {doc.metadata}, content: {doc.page_content}\n"


context = list(doc_to_str(docs))

model_id = "gpt-3.5-turbo-0125"
temperature = 0
response_model = ChatOpenAI(model=model_id, temperature=temperature)

system_prompt_template = "You are a helpful assistant who is answering questions about movies. Your name is Carl."
response_prompt_template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Be convrsational but use three sentences maximum.
{context}

Question: {question}
Helpful Answer:"""
messages = [
    SystemMessagePromptTemplate.from_template(system_prompt_template),
    HumanMessagePromptTemplate.from_template(response_prompt_template),
]
rag_prompt = ChatPromptTemplate.from_messages(messages)

rag_chain = {"context": retriever, "question": RunnablePassthrough()} | rag_prompt | response_model | StrOutputParser()

raw_context = retriever.invoke("What are some movies about dinosaurs")
compressed_context = "".join(doc_to_str(docs))
print(compressed_context)
questions = ["What is the movie about dinosaurs?", "What is the movie about dreams?", "What's your name?"]
for q in questions:
    out = rag_chain.invoke(input=dict(context=compressed_context, question=q))
    print(out)

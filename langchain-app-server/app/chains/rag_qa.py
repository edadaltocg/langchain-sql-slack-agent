from operator import itemgetter

from langchain.prompts import ChatPromptTemplate
from langchain.schema.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel, RunnablePassthrough, chain
from langchain_openai import ChatOpenAI
from langserve.schema import CustomUserType

store = {}


class AssistantInput(CustomUserType):
    input: str
    session_id: str


def make_conversational_rag_chain(
    docs_retriever,
    people_retriever,
    docs_to_str,
    people_to_str,
):
    system_prompt_template = """
You are an assistant for data question-answering tasks. \
Use the following pieces of retrieved context and people to answer the question. \
If you don't know the answer, just say that you don't know. \
Be concise in your response. Never repeat yourself on follow up responses.

# Instruction
Inform the user with all relevant columns and all relevant tables to look. \
Tag one relevant person with @<person name> who might know the answer, but only if necessary and only on the first message.

# Objective
You aim to identify potential features and target variable for the analysis.

# Audience
Data Scientists

# Context:
{context}

# People:
{people}

# Chat History:
{chat_history}

Let's think step-by-step.
"""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt_template),
            ("human", "{question}"),
        ]
    )

    query_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=1)
    llm = ChatOpenAI(model="gpt-4-turbo-2024-04-09", temperature=1)

    @chain
    def get_session_history(input_dict: dict[str, str]):
        session_id = input_dict.get("session_id", "123")
        if session_id not in store:
            store[session_id] = []
        input_dict["chat_history"] = store[session_id]
        print(input_dict)
        return input_dict

    @chain
    def set_messages(kwargs):
        session_id = kwargs["past"]["session_id"]
        question = kwargs["past"]["question"]
        store[session_id].append(f"User: {question}")
        resp = kwargs["llm"]
        content = resp.content
        store[session_id].append(f"Assistant: {content}")
        return resp

    contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is.

Chat History:
{chat_history}
"""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            ("human", "{input}"),
        ]
    )

    rag_chain = (
        get_session_history
        | {
            "question": itemgetter("input"),
            "session_id": itemgetter("session_id"),
            "chat_history": itemgetter("chat_history"),
            "context": contextualize_q_prompt | llm | StrOutputParser() | docs_retriever | docs_to_str,
            "people": contextualize_q_prompt | llm | StrOutputParser() | people_retriever | people_to_str,
        }
        | RunnableParallel({"llm": prompt | llm, "past": RunnablePassthrough()})
        | set_messages
    )

    return rag_chain

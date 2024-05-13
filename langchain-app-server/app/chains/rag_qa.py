from operator import itemgetter
from pprint import pprint
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField, RunnableParallel, RunnablePassthrough, chain
from langchain_openai import ChatOpenAI
from langserve.schema import CustomUserType
from pydantic import BaseModel, Field
from typing import Any, List, Optional, Sequence, Tuple, Union

store: dict[str, list[str]] = {}


class InputDict(BaseModel):
    question: str
    session_id: str
    chat_history: list[str] = Field(
        [],
        extra={"widget": {"type": "chat", "input": "question", "output": "answer"}},
    )


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
Human: {question}
AI: """

    prompt = ChatPromptTemplate.from_template(system_prompt_template)

    temperature = 0
    query_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=temperature)
    llm = ChatOpenAI(model="gpt-4-turbo-2024-04-09", temperature=temperature)

    @chain
    def get_session_history(input_dict: dict[str, Any]):  # InputDict):
        if isinstance(input_dict, dict):
            input_dict = InputDict(**input_dict)
        session_id = input_dict.session_id
        if session_id not in store:
            store[session_id] = []
        input_dict.chat_history = store[session_id]
        # transform to dict for the next step
        input_dict_ = input_dict.dict()
        return input_dict_

    @chain
    def set_messages(kwargs):
        session_id = kwargs["past"]["session_id"]
        question = kwargs["past"]["question"]
        store[session_id].append(f"Human: {question}")
        resp = kwargs["llm"]
        content = resp.content
        store[session_id].append(f"AI: {content}")
        pprint(kwargs)
        return content

    contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is.

Chat History:
{chat_history}
Follow Up Question: {question}
Standalone Question: """
    contextualize_q_prompt = ChatPromptTemplate.from_template(contextualize_q_system_prompt)

    rag_chain = (
        get_session_history
        | {
            "question": itemgetter("question"),
            "session_id": itemgetter("session_id"),
            "chat_history": itemgetter("chat_history"),
            "context": contextualize_q_prompt | query_llm | StrOutputParser() | docs_retriever | docs_to_str,
            "people": contextualize_q_prompt | query_llm | StrOutputParser() | people_retriever | people_to_str,
        }
        | RunnableParallel({"llm": prompt | llm, "past": RunnablePassthrough()})
        | set_messages
    )

    return rag_chain
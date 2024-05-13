from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import OpenAI, ChatOpenAI

from pydantic import BaseModel, Field
from typing import List, Optional, Sequence, Tuple, Union


class ChatRequest(BaseModel):
    question: str
    chat_history: List[Tuple[str, str]] = Field(
        ...,
        extra={"widget": {"type": "chat", "input": "question", "output": "answer"}},
    )


llm = ChatOpenAI(temperature=0)
memory = ConversationBufferMemory(return_messages=False)
chain = ConversationChain(
    llm=llm,
    verbose=True,
    memory=memory,
)

if __name__ == "__main__":
    query1 = "What is the capital of France?"
    response1 = chain.invoke(query1)
    print(response1)
    query2 = "And what about Spain?"
    response2 = chain.invoke(query2)
    print(response2)
import logging
import os

from langchain.schema import AIMessage
from langserve import RemoteRunnable
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

logging.basicConfig(level=logging.DEBUG)

conversational_rag_chain = RemoteRunnable(
    f"http://{os.environ.get('REMOTE_HOST', 'localhost')}:{os.environ.get('REMOTE_PORT', '8000')}/rag-conversational/"
)

app = App(token=os.environ["SLACK_BOT_TOKEN"], signing_secret=os.environ["SLACK_SIGNING_SECRET"])


@app.event("app_mention")
def handle_mentions(body, say, logger):
    logger.debug(body)

    event = body["event"]
    logger.info(event)

    user_id = event["user"]
    logger.debug(f"User ID: {user_id}")

    user_message = event["text"].replace("<@U072EBQNMUH>", "").strip()
    logger.debug(f"User Message: {user_message}")

    thread_ts = event.get("thread_ts", None) or event["ts"]
    logger.debug(f"Thread TS: {thread_ts}")

    try:
        response: AIMessage = conversational_rag_chain.invoke(
            {"question": user_message, "session_id": thread_ts},
            # config={"configurable": {"session_id": thread_ts}},
        )
        logger.debug(f"Response: {response}")
        say(text=response, thread_ts=thread_ts)

    except Exception as e:
        say(text="An error occurred. Please try again later.", thread_ts=thread_ts)
        logger.error(f"Error handling mention: {e}")


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

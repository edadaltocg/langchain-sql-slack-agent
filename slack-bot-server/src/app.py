import os
import logging

logging.basicConfig(level=logging.DEBUG)

# Use the package we installed
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from slack_bolt.async_app import AsyncApp
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap
from langserve import RemoteRunnable

chat = RemoteRunnable("http://localhost:8100/openai/")
# Initialize your app with your bot token and signing secret
app = App(token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))


# New functionality
@app.event("app_mention")
def handle_mentions(body, say, logger):
    try:
        logger.info(body)
        user_id = body["event"]["user"]
        user_message = body["event"]["text"]
        logger.info(f"User ID: {user_id}")
        logger.info(f"User Message: {user_message}")
        # Send a message to the channel
        # say(f"Hello <@{user_id}>! I'm a memoryless bot. I can't remember anything.")
        response = chat.invoke(user_message)
        logger.info(f"Response: {response}")
        output_message = response.content
        logger.info(f"Output Message: {output_message}")
        say(output_message)
    except Exception as e:
        logger.error(f"Error handling mention: {e}")


# Ready? Start your app!
if __name__ == "__main__":
    # app.start(port=int(os.environ.get("SLACK_BOT_PORT", 3000)))
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

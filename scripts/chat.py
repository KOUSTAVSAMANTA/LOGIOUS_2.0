from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from pymongo import MongoClient
from langchain.pydantic_v1 import BaseModel,Field
from langchain_core.messages import HumanMessage
import os
from PIL import Image
import requests
import threading
import time
import datetime
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
from langchain.tools import DuckDuckGoSearchRun
import os
import google.generativeai as genai
import re


# meory gate ---------------------------------------------------------
client = MongoClient("mongodb+srv://koustavsamanta007:5SeA3PVKxX5wMBG4@cluster0.juvm5eq.mongodb.net/logious-db?retryWrites=true&w=majority&appName=Cluster0",
ssl = True
)
db = client['AUTH']
collection = db['Authentication']
collection2 = db['Memory']
memory_key = "chat_history"
_MEMORY_ =ConversationBufferMemory(memory_key=memory_key)

def load_or_create_memory(user_id, collection2):
  """Loads the memory for a user if the user ID exists in the database.
  If the user ID does not exist, creates a new memory.

  Args:
    user_id: The user ID to check for.
    collection2: The collection2 to check in.

  Returns:
    The memory for the user.
  """

  if collection2.find_one({"user_id": user_id}) is not None:
    _mem = ConversationBufferMemory(memory_key=memory_key)
    memory = collection2.find_one({"user_id": user_id})["memory_key"]
    for i in memory:
        try:
            _mem.chat_memory.add_user_message(i['Human'])
            _mem.chat_memory.add_ai_message(i['AI'])
        except Exception as e:
            pass
    return _mem
  else:
    memory = ConversationBufferMemory(memory_key=memory_key)
    return memory
def check_user(user_id, memory_key, collection2):
  """Checks if a user is present in the collection2.
  If present, updates the entry.
  If not present, creates a new entry.

  Args:
    user_id: The user ID to check for.
    memory_key: The memory key to update or create.
    collection2: The collection2 to check in.

  Returns:
    True if the user is present, False otherwise.
  """

  if collection2.find_one({"user_id": user_id}) is not None:
    collection2.update_one(
        {"user_id": user_id}, {"$set": {"memory_key": memory_key}})
    return "updated"
  else:
    collection2.insert_one({"user_id": user_id, "memory_key": memory_key})
    return "created"
def delete_entry(user_id, collection2):
  """Deletes an entry from a collection2 where the user ID matches.

  Args:
    user_id: The user ID to match.
    collection2: The collection2 to delete from.
  """

  collection2.delete_one({"user_id": user_id})
  return f"Deleted Previous Conversations with {user_id}"

# --------------------------------------------------------------------
#  THe API KEY
os.environ["GOOGLE_API_KEY"] = "AIzaSyDqKzb2p4ItiEEao-oim5IcGgAifOtv6do"

template = """You are a nice chatbot having a conversation with a human.your name is LOGIOUS powerd by CODA.

Previous conversation:
{chat_history}

New human question: {question}
Response:"""


def clear_memory(userId):
    z = delete_entry(user_id=userId, collection2=collection2)
    return "Memory cleared !! "+z
# Display assistant response in chat message container
llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro-001", temperature=0.9)


def get_res_chat(q,userID,img):
    if img != "null":

        llmv = ChatGoogleGenerativeAI(model='gemini-1.0-pro-vision-latest', safety_settings=None, )
        # Construct the full file path
        file_path = os.path.join('./DATA', img)

        # Open the image using the full file path
        image = Image.open(file_path)

        memory = load_or_create_memory(user_id=userID, collection2=collection2)
        # print(memory)
        full_response = ""
        prompt_t = """You are a nice chatbot having a conversation with a human.your name is LOGIOIUS powerd by CODA.

                    Previous conversation:
                    {chat_history}

                    New human question: {question}
                    Response:"""
        # print(prompt)
        hmessage1 = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": q,
                },  # You can optionally provide text parts
                {"type": "image_url", "image_url": image},
            ]
        )
        z = llmv.invoke([hmessage1])

        assistant_response = z.content

        memory.save_context({"input": q + str(img)}, {"output": assistant_response})
        z = memory.chat_memory.messages
        # st.write(z)
        mem = []
        for i in range(0, len(z), 2):
            mem.append({"Human": z[i].content, "AI": z[i + 1].content})
        # print(mem)
        # print(userid.id)
        ch = check_user(user_id=userID, memory_key=mem, collection2=collection2)
        print(ch)
        return assistant_response
    else:

    # memory_key = "chat_history"
        global _MEMORY_
        # memory = st.session_state.memory
        # memory =ConversationBufferMemory(memory_key=memory_key)
        memory = load_or_create_memory(user_id=userID, collection2=collection2)
        _MEMORY_ = memory

        prompt_t = PromptTemplate.from_template(template)

        # Notice that we need to align the `memory_key`
        conversation = LLMChain(
            llm=llm,
            prompt=prompt_t,
            verbose=True,
            memory=memory,
            output_parser=StrOutputParser()
        )
        z = conversation({"question": q})
        assistant_response = z['text']
        # Simulate stream of response with milliseconds delay

        print(type(memory))
        z = memory.chat_memory.messages
        mem = []
        for i in range(0, len(z), 2):
            mem.append({"Human": z[i].content, "AI": z[i + 1].content})
        print(mem)
        # print(userid.id)
        ch = check_user(user_id=userID, memory_key=mem, collection2=collection2)
        # if st.button("clear memory"):
        # print(ch)
        return assistant_response

# print(get_res_chat("explain the conent of the image","662778d46b0fb6a83daedb6b662778fd6b0fb6a83daedb76","b_4.png"))


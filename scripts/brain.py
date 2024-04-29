from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from pymongo import MongoClient
from langchain.pydantic_v1 import BaseModel,Field

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

search = DuckDuckGoSearchRun()
def custome_search(i):
    k = search.run(i)
    template_search = """understand the Result and return the explained version of the Result and all the main points.
    Result: {question}
    Response:"""
    llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro-001")
    prompt_t = PromptTemplate.from_template(template_search)
    conversation = LLMChain(
        llm=llm,
        prompt=prompt_t,
        verbose=True,
        output_parser=StrOutputParser()
    )
    z = conversation({"question": k})
    return z['text']


# search = SerpAPIWrapper()
search_toolkit = Tool(
        name="Search",
        func=custome_search,
        description="The Search Toolkit is your ultimate companion for navigating the vast expanse of the internet. Whether you're seeking answers, conducting research, or exploring new interests, this powerful tool ensures accurate and comprehensive results every time. Powered by DuckDuckGoSearchRun, it delivers precisely what you need to know, when you need it. Say goodbye to endless scrolling and irrelevant results – with the Search Toolkit, accessing information has never been easier.you have access to internet via this tool."
    )
def get_current_time_and_date():
    current_time_and_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return "current date is "+current_time_and_date.split()[0]+" current time is "+current_time_and_date.split()[1]

def tool_less_answering(k):
    template_search = """You are a nice chatbot having a conversation with a human.your name is Logious powered by LOGIC Developed by CODA.you can respond all question.Think Carefully.
                        New human question: {question}"""
    llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro-001")
    prompt_t = PromptTemplate.from_template(template_search)
    memory = _MEMORY_
    conversation = LLMChain(
        llm=llm,
        prompt=prompt_t,
        verbose=True,
        memory=memory,
        output_parser=StrOutputParser()
    )
    z = conversation({"question": k})
    return z['text']


multinomial_toolkit = Tool(
    name="QA",
    func=tool_less_answering,
    description = "The Tool-less Answering function is your indispensable assistant for seamlessly responding to human queries with the power of AI. Whether you're addressing inquiries, providing information, or engaging in conversation, this function ensures prompt and insightful responses every time. Powered by Gemini-1.0-pro-001, it harnesses the capabilities of advanced language models to deliver accurate and contextually relevant answers in real-time. Bid farewell to manual searching and cumbersome interfaces – with Tool-less Answering, facilitating meaningful interactions has never been more effortless. You have the ability to tap into the wealth of knowledge available via this function.Any tool having Action None or Action Input None can use this tool.it acts as a Fallback tool.this tool also gives you the ability to think"

)

current_date_time_tool = Tool.from_function(
    func=lambda input_text: get_current_time_and_date(),
    name="CurrentDateTime",
    description="Provides the current date and time in from of a string"
)


tools = [search_toolkit,current_date_time_tool,multinomial_toolkit]

template = """Answer the following questions as best you can. 
information about yourself is your name is LOGIOUS you are able to answer any question you are developed by Koustav powered by CODA.you can thinK.
you can use the tool named Search to get anything from the internet.
if you need to think you can use the tool QA.
Only use a tool if needed, otherwise respond with Final Answer.
CurrentDateTime returns a string where date is given in %Y-%m-%d format followed by time given in %H:%M:%S format
you need to get the time and date every time to keep track of the environment

NOTE: all actions take input as string format
You have access to the following tools:

{tools}

Use the following format:

Conversations:{chat_history}
Question: the input question you must answer
Thought: you should only think about what to do if you need.your thinking will be based on the Question and chat_history
Action: the name of the tool to be used from the given Tools:-{tool_names}
Action Input: the input to the action it should be a string sentence and should be related to the Thought.it should not look like func(query) instead it should directly give the query.
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat maximum 4 times)
Thought: I now know the final answer.if you don't know then return the final observation as the Final Answer.
Final Answer: the final answer to the original input question.

Begin!

Question: {input}
{agent_scratchpad}"""


class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)

class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise OutputParserException(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)

prompt = CustomPromptTemplate(
    template=template,
    tools=tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    input_variables=["input", "chat_history","intermediate_steps"]
)

def get_res(q,userID):
    output_parser = CustomOutputParser()
    llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro-001",temperature=0.9)
    # memory_key = "chat_history"
    global _MEMORY_
    # memory = st.session_state.memory
    # memory =ConversationBufferMemory(memory_key=memory_key)
    memory = load_or_create_memory(user_id=userID, collection2=collection2)
    _MEMORY_ = memory
    print(memory)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    tool_names = [tool.name for tool in tools]
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["Observation"],
        allowed_tools=tool_names,

    )
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True,memory=memory,handle_parsing_errors=True)
    assistant_response = agent_executor.run(q)
    z = memory.chat_memory.messages
    mem = []
    for i in range(0, len(z), 2):
        mem.append({"Human": z[i].content, "AI": z[i + 1].content})
    print(mem)
    # print(userid.id)
    ch = check_user(user_id=userID, memory_key=mem, collection2=collection2)
    print(ch)
    return assistant_response

# # Global flag variable to control the thread
# stop_flag = False
# data = {}
# data_lock = threading.Lock()

# def make_request(url):
#     global stop_flag
#     global data
#     global data_lock
#     while not stop_flag:
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 with data_lock:
#                     data = response.json()
#             else:
#                 print(f"Failed to make GET request. Status code: {response.status_code}")
#             time.sleep(1)  # Wait for 1 second before making the next request
#         except Exception as e:
#             pass
#     print("Stopping request thread...")

# def main():
#     # global stop_flag
#     # global data
#     # global data_lock
#     # URL to send GET requests to
#     # url = "http://127.0.0.1:8000/get_task"
#
#     # Create a thread for making requests
#     # request_thread = threading.Thread(target=make_request, args=(url,))
#
#     # Start the thread
#     # request_thread.start()
#
#     # Your main loop for user input and getting response
#     while True:
#         query = input("Enter query: ")
#         if query.lower() == 'exit':
#             stop_flag = True
#             break
#         # elif query == 'data':
#         #     with data_lock:
#         #         print(data)
#
#         elif "set" in query:
#             f = open("data.txt", "w")
#             current_time = datetime.datetime.now()
#             f.write(current_time.strftime("%Y-%m-%d %H:%M:%S"))
#             f.close()
#         else:
#             print(get_res(query))
#
#     # Wait for the request thread to finish
#     # request_thread.join()
#     print("Main thread finished")
#
# if __name__ == "__main__":
#     main()

import os
from dotenv import load_dotenv

from operator import itemgetter

from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import ConversationChain
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain.tools.render import render_text_description_and_args

from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)


load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")
secrets_file = os.environ.get("SECRETS_FILE")


system_prompt = """Respond to the human as helpfully and accurately as possible. You have access to the following tools:

{tools}

Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or {tool_names}

Provide only ONE action per $JSON_BLOB, as shown:

{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}


Follow this format:

Question: input question to answer
Thought: consider previous and subsequent steps
Action:
$JSON_BLOB
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
{{
  "action": "Final Answer",
  "action_input": "Final response to human"
}}

Here are some examples of valid $JSON_BLOBs:
{{
  "action": "create_gmail_draft",
  "action_input": {{
    "message": "Hello, this is a draft!",
    "to": ["recipient1@example.com", "recipient2@example.com"],
    "subject": "Meeting",
    "cc": ["cc1@example.com"],
    "bcc": ["bcc1@example.com"]
  }}
}}
{{
  "action": "send_gmail_message",
  "action_input": {{
    "message": "Hello, this is the email content.",
    "to": ["recipient@example.com"],
    "subject": "Meeting",
    "cc": ["cc@example.com"],
    "bcc": ["bcc@example.com"]
  }}
}}
{{
  "action": "search_gmail",
  "action_input": {{
    "query": "from:sender@example.com subject:important",
    "resource": "messages",
    "max_results": 5
  }}
}}
{{
  "action": "get_gmail_message",
  "action_input": {{
    "message_id": "unique_message_id"
  }}
}}
{{
  "action": "get_gmail_thread",
  "action_input": {{
    "thread_id": "unique_thread_id"
  }}
}}
```

Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation"""


human_prompt = """{text}

{agent_scratchpad}
 (reminder to respond in a JSON blob no matter what)"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", human_prompt),
    ]
)

credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file=secrets_file,
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)

tools = toolkit.get_tools()

llm = ChatGoogleGenerativeAI(
    model="gemini-pro", google_api_key=api_key, convert_system_message_to_human=True
)

pre_agent = (
    {
        "text": itemgetter("text"),
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
    }
    | prompt
    | llm
    | JSONAgentOutputParser()
)
agent = AgentExecutor(agent=pre_agent, tools=tools, verbose=True)


def generate_draft(user_input):
    data = {"input": user_input}
    return agent.invoke(data)

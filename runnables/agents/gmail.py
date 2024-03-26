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

from config.prompt_templates import gmail_system_prompt, gmail_human_prompt


load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")
secrets_file = os.environ.get("SECRETS_FILE")


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", gmail_system_prompt),
        ("human", gmail_human_prompt),
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

from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder


chatbot_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant called Yara.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

summary_prompt_template = PromptTemplate.from_template(
    """Write a concise summary of the following:
                "{text}"
                Be as brief as possible, but include all the key points.
                CONCISE SUMMARY:"""
)

retrieval_qa_template = """Use the following pieces of context to answer the user's question. 
Keep the answers very brief and if you don't know the answer, 
just say that you don't know, don't try to make up an answer.
----------------
{context}"""


gmail_system_prompt = """Respond to the human as helpfully and accurately as possible. You have access to the following tools:

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

gmail_human_prompt = """{text}

{agent_scratchpad}
 (reminder to respond in a JSON blob no matter what)"""

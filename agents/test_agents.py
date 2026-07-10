


from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import dynamic_prompt, ModelRequest, before_model, after_model
from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from langgraph.runtime import Runtime

load_dotenv()
import os

@dataclass
class Context:
    user_name: str

# Dynamic prompts
@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest) -> str:
    user_name = request.runtime.context.user_name
    system_prompt = f"You are a helpful assistant. Address the user as {user_name}."
    return system_prompt

# Before model hook
@before_model
def log_before_model(state: AgentState, runtime: Runtime[Context]) -> dict | None:
    print(f"log_before_model: {state}")
    print(f"Processing request for user: {runtime.context.user_name}")
    return None

# After model hook
@after_model
def log_after_model(state: AgentState, runtime: Runtime[Context]) -> dict | None:
    print(f"log_after_model: {state}")
    print(f"Completed request for user: {runtime.context.user_name}")
    return None


from langchain.chat_models import init_chat_model

custom_profile = {
                  "max_input_tokens": 400000,
                  "image_inputs": True,
                  "reasoning_output": True,
                  "tool_calling": True
                }

from langchain_core.rate_limiters import InMemoryRateLimiter

limit = InMemoryRateLimiter(requests_per_second=0.1, check_every_n_seconds=0.1, max_bucket_size=10)
# llm = init_chat_model(model='deepseek-v4-flash', api_key=os.getenv('DEEPSEEK_API_KEY', ''), rate_limiter=limit)

llm = init_chat_model(model='qwen3.5-plus', model_provider='openai', api_key=os.getenv('LLM_API_KEY', ''), base_url=os.getenv('LLM_BASE_URL', ''), streaming=True)

# llm = ChatOpenAI(model=os.getenv('LLM_MODEL_ID', 'qwen-plus'), api_key=os.getenv('LLM_API_KEY', ''), base_url=os.getenv('LLM_BASE_URL', ''), streaming=True)
#
# agent = create_agent(
#     model=llm,
#     tools=[],
#     middleware=[dynamic_system_prompt, log_before_model, log_after_model],
#     context_schema=Context
# )

@tool
def get_weather(req: ToolRuntime, city: str) -> str:
    """根据城市查询天气，返回天气信息"""
    writer = req.stream_writer
    writer(f'get weather from {city}')
    print(333, req.context.user_id)
    return '晴天'


from langchain.agents import create_agent
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

def get_user_info() -> str:
    """Look up information about the current user."""
    return "No user profile on file."

from langchain.messages import AIMessageChunk
async def invoke(agent, messages, config):
    async for msg, meta in agent.astream(messages, stream_mode='messages', config=config):

        if isinstance(msg, AIMessageChunk):
            if msg.content:
                yield msg.content

DB_URI = "postgresql://postgres:690903@localhost:5432/postgres?sslmode=disable"
async with AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup() # auto create tables in PostgreSQL
    agent = create_agent(
        llm,
        tools=[],
        checkpointer=checkpointer,
    )
    message_1 = {'messages': [{'role': 'user', 'content': "你好，我叫Rick"}]}


    res1 = invoke(agent, message_1, config={'configurable': {'thread_id': 3}})
    print(res1)

    message_2 = {'messages': [{'role': 'user', 'content': "你还记得我是谁吗？"}]}

    res2 = invoke(agent, message_1, config={'configurable': {'thread_id': 3}})
    print(res2['messages'][-1].content)






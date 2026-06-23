import os
from abc import ABC, abstractmethod
from typing import List, Any

from langchain.agents import create_agent
from langchain.messages import HumanMessage, AIMessageChunk
from langchain_openai import ChatOpenAI
from langgraph.graph.state import CompiledStateGraph

from utils.logger import log


class BaseAgent(ABC):

    def __init__(self, model_name=None, api_key=None, base_url=None, stream=False):

        if model_name is None:
            self.__model_name = model_name or os.getenv('LLM_MODEL_ID', 'qwen-plus')

        if api_key is None:
            self.__api_key = api_key or os.getenv('LLM_API_KEY', '')

        if base_url is None:
            self.__base_url = base_url or os.getenv('LLM_BASE_URL', '')

        self.stream = stream
        self.tools = None
        self.system_prompt = None
        self.llm = None
        self.agent: CompiledStateGraph = None

    async def build_agent(self):
        self.system_prompt = self.get_system_prompt()

        if not self.tools:
            self.tools = await self.build_tools()

            tool_names = [tool.name for tool in self.tools]
            log.info(f'{self.__class__.__name__} Tools: {tool_names}')

        self.llm = ChatOpenAI(model=self.__model_name, api_key=self.__api_key, base_url=self.__base_url, streaming=self.stream)

        self.agent = create_agent(model=self.llm, tools=self.tools, system_prompt=self.system_prompt)


    @abstractmethod
    def get_system_prompt(self) -> str:
        pass


    @abstractmethod
    def get_user_prompt(self, msg) -> str:
        pass


    @abstractmethod
    async def build_tools(self) -> List:
        pass


    async def run(self, req: Any):
        if self.agent is None:
            await self.build_agent()

        messages = {
            'messages': [
                HumanMessage(content=self.get_user_prompt(req))
            ]
        }

        token_usage = {'input': 0, 'output': 0, 'total': 0}
        async for msg, meta in self.agent.astream(messages, stream_mode='messages'):

            if isinstance(msg, AIMessageChunk):
                if msg.content:
                    yield msg.content


            if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
                token_usage['input'] += msg.usage_metadata.get('input_tokens', 0)
                token_usage['output'] += msg.usage_metadata.get('output_tokens', 0)
                token_usage['total'] += msg.usage_metadata.get('total_tokens', 0)

        log.info(f'{self.__class__.__name__}本次token使用：{token_usage}')
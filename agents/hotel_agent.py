import os

from langchain_mcp_adapters.client import MultiServerMCPClient

from agents.base_agent import BaseAgent
from agents.prompts.hotel_prompt import HOTEL_PROMPT
from agents.service.mcp_service import limit_amap
from models.schema import Request


class HotelAgent(BaseAgent):

    def __init__(self, model_name=None, api_key=None, base_url=None, stream=False):
        super().__init__(model_name, api_key, base_url, stream)

    def get_system_prompt(self) -> str:
        return HOTEL_PROMPT

    def get_user_prompt(self, request: Request):
        user_prefer = ''
        if request.hotel_prefer:
            user_prefer = request.hotel_prefer

        return f'使用maps_text_search工具搜索{request.end_city}的{user_prefer}酒店'


    async def build_tools(self):

        amap_key = os.getenv('AMAP_API_KEY', None)
        if not amap_key:
            raise ValueError('env文件中未配置AMAP_API_KEY，请检查！')
        mcp_info = {
            'amap': {
                'url': f'https://mcp.amap.com/sse?key={amap_key}',
                'transport': 'sse',
                'timeout': 20
            }
        }
        mcp_client = MultiServerMCPClient(mcp_info, tool_interceptors=[limit_amap])

        tools = await mcp_client.get_tools()
        return tools


if __name__ == '__main__':
    async def main():
        agent = HotelAgent(stream=True)
        request = Request(start_city='南京', end_city='丽江', start_date='2026-07-01', end_date='2026-07-03', hotel_prefer=['豪华型'])
        async for content in agent.run(request):
            print(content, end='', flush=True)

    import asyncio
    asyncio.run(main())


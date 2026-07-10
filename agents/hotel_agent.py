from agents.base_agent import BaseAgent
from agents.prompts.hotel_prompt import HOTEL_PROMPT
from agents.service.mcp_service import get_amap_tools
from models.schema import Request


class HotelAgent(BaseAgent):

    def get_system_prompt(self) -> str:
        return HOTEL_PROMPT

    def get_user_prompt(self, request: Request):
        user_prefer = ''
        if request.hotel_prefer:
            user_prefer = request.hotel_prefer

        return f'使用maps_text_search工具搜索{request.end_city}的{user_prefer}酒店'


    async def build_tools(self):

        return await get_amap_tools()


if __name__ == '__main__':
    async def main():
        agent = HotelAgent(stream=True)
        request = Request(start_city='南京', end_city='丽江', start_date='2026-07-01', end_date='2026-07-03', hotel_prefer=['豪华型'])
        async for content in agent.run(request):
            print(content, end='', flush=True)

    import asyncio
    asyncio.run(main())


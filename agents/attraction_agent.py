from agents.base_agent import BaseAgent
from agents.prompts.attraction_prompt import ATTRACTION_PROMPT
from agents.service.mcp_service import get_amap_tools
from models.schema import Request


class AttractionAgent(BaseAgent):

    def get_system_prompt(self) -> str:
        return ATTRACTION_PROMPT

    def get_user_prompt(self, request: Request):
        user_prefer = ''
        if request.attraction_prefer:
            user_prefer = request.attraction_prefer

        return f'使用amap工具搜索{request.end_city}的{user_prefer}景点'


    async def build_tools(self):

        return await get_amap_tools()


if __name__ == '__main__':
    async def main():
        agent = AttractionAgent(stream=True)
        request = Request(start_city='南京', end_city='丽江', start_date='2026-06-22', end_date='2026-06-24', attraction_prefer=['公园'])
        async for content in agent.run(request):
            print(content, end='', flush=True)

    import asyncio
    asyncio.run(main())


from agents.base_agent import BaseAgent
from agents.prompts.weather_prompt import WEATHER_PROMPT
from agents.service.mcp_service import get_amap_tools
from models.schema import Request


class WeatherAgent(BaseAgent):

    def get_system_prompt(self) -> str:
        return WEATHER_PROMPT

    def get_user_prompt(self, request: Request):
        return f'使用amap工具搜索{request.end_city}{request.start_date}至{request.end_date}的天气'


    async def build_tools(self):

        return await get_amap_tools()


if __name__ == '__main__':
    async def main():
        agent = WeatherAgent(stream=True)
        request = Request(start_city='南京', end_city='丽江', start_date='2026-07-04', end_date='2026-07-05', thread_id='4')
        async for content in agent.run(request):
            print(content, end='', flush=True)

    import asyncio

    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )
    asyncio.run(main())


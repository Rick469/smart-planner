from typing import Any

from agents.base_agent import BaseAgent
from agents.hotel_agent import HotelAgent
from agents.weather_agent import WeatherAgent
from agents.attraction_agent import AttractionAgent
from agents.planner_agent import PlannerAgent
from models.schema import Request
from utils.logger import log


if __name__ == '__main__':
    import time
    import asyncio
    from agents.service.agent_service import agent_run


    async def main():
        a_agent = AttractionAgent(stream=True)
        h_agent = HotelAgent(stream=True)
        w_agent = WeatherAgent(stream=True)
        p_agent = PlannerAgent(stream=True)
        request = Request(start_city='南京', end_city='丽江', start_date='2026-06-22', end_date='2026-06-23')

        attractions, hotels, weather = await asyncio.gather(
            agent_run(a_agent, request),
            agent_run(h_agent, request),
            agent_run(w_agent, request)
        )

        log.info(f'景点信息：{attractions}')

        log.info(f'酒店信息：{hotels}')

        log.info(f'天气信息：{weather}')

        req = {'request': request, 'attractions': attractions, 'hotels': hotels, 'weather': weather}
        planner = await agent_run(p_agent, req)

        log.info(f'旅程信息：{planner}')

    before = time.time()

    asyncio.run(main())

    after = time.time()
    duration = after - before
    log.info(f'耗时：{duration}秒')

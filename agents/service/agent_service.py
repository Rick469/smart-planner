import asyncio
import time
from typing import Any

from agents.base_agent import BaseAgent
from models.schema import Request
from utils.logger import log


async def agent_run(agent: BaseAgent, req: Any):
    """多agent并发执行请求"""
    before = time.time()
    res = ''
    async for content in agent.run(req):
        res += content

    after = time.time()
    log.info(f'{str(agent)}执行：{after-before}秒')
    return res


async def plan(request: Request, a_agent, h_agent, w_agent, p_agent):

    attractions, hotels, weather = await asyncio.gather(
        agent_run(a_agent, request),
        agent_run(h_agent, request),
        agent_run(w_agent, request)
    )

    log.info(f'景点信息：{attractions}')

    log.info(f'酒店信息：{hotels}')

    log.info(f'天气信息：{weather}')

    request.weather_result = weather
    request.attractions_result = attractions
    request.hotel_result = hotels

    async for content in p_agent.run(request):
        yield content

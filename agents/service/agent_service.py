import time
from typing import Any

from agents.base_agent import BaseAgent
from models.schema import Request
import asyncio
from utils.logger import log
from models.workflow import WorkflowEvent, WorkflowEventType


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

    yield WorkflowEvent(
        type=WorkflowEventType.TOOL_START,
        tool="weather",
        title="查询天气"
    )

    yield WorkflowEvent(
        type=WorkflowEventType.TOOL_START,
        tool="hotel",
        title="查询酒店"
    )

    yield WorkflowEvent(
        type=WorkflowEventType.TOOL_START,
        tool="attraction",
        title="查询景点"
    )

    attractions, hotels, weather = await asyncio.gather(
        agent_run(a_agent, request),
        agent_run(h_agent, request),
        agent_run(w_agent, request)
    )

    yield WorkflowEvent(
        type=WorkflowEventType.TOOL_END,
        tool="weather"
    )

    yield WorkflowEvent(
        type=WorkflowEventType.TOOL_END,
        tool="hotel"
    )

    yield WorkflowEvent(
        type=WorkflowEventType.TOOL_END,
        tool="attraction"
    )

    log.info(f"景点信息：{attractions}")
    log.info(f"酒店信息：{hotels}")
    log.info(f"天气信息：{weather}")

    request.weather_result = weather
    request.attractions_result = attractions
    request.hotel_result = hotels

    yield WorkflowEvent(
        type=WorkflowEventType.THINKING_START,
        title="生成旅行规划"
    )

    yield WorkflowEvent(
        type=WorkflowEventType.THINKING_END
    )

    async for token in p_agent.run(request):

        yield WorkflowEvent(
            type=WorkflowEventType.TOKEN,
            content=token
        )



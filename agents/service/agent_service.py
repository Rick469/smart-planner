import time

from agents.base_agent import BaseAgent
from typing import Any
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
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


def amap_client():
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
    mcp_client = MultiServerMCPClient(mcp_info)

    return mcp_client
import asyncio
import json
import hashlib
import os
from copy import deepcopy

from langchain_mcp_adapters.client import MultiServerMCPClient
from mcp.types import TextContent, CallToolResult
from openai.resources.containers.files import content

from agents.service.sqlite_service import PlannerDB
from langchain_mcp_adapters.interceptors import MCPToolCallRequest
from utils.logger import log


GLOBAL_AMAP_SEM = asyncio.Semaphore(3)
GLOBAL_TOOL_CACHE = None

async def limit_amap(request: MCPToolCallRequest, handler):
    tool_name = request.name or ""
    args = deepcopy(request.args)
    log.info(f'args: {args}')
    cache_key = make_cache_key(args)
    db = PlannerDB()
    cache_value = db.get_cache(cache_key)
    log.info(f'cache_key: {cache_key}，cache_value: {cache_value}')
    if cache_value:
        log.info(f'命中cache，return')
        result = CallToolResult(isError=False, content=[TextContent(type='text', text=cache_value)])
        return result

    # 只控制高德工具
    if "amap_" in tool_name or "maps_" in tool_name:
        # ⭐执行层限流
        async with GLOBAL_AMAP_SEM:
            log.info(f"【limited tools】： {tool_name}")
            result = await handler(request)

            # 存入cache
            db.set_cache(cache_key, json.dumps(result.content[0].text))
            return result
    else:
        log.info(f'【non-limited tools】: {tool_name}')
        result = await handler(request)

        # 存入cache
        db.set_cache(cache_key, json.dumps(result.content[0].text))
        return result


def normalize_input(tool_input: dict):

    def clean(obj):
        if isinstance(obj, dict):
            return {
                k: clean(v)
                for k, v in obj.items()
                if v is not None and v != ""
            }

        if isinstance(obj, list):
            return [clean(x) for x in obj]

        if isinstance(obj, str):
            return obj.strip()

        return obj

    return clean(tool_input)


def make_cache_key(tool_input: dict):

    normalized = normalize_input(tool_input)

    # ⭐关键：稳定序列化
    text = json.dumps(
        normalized,
        sort_keys=True,          # 解决 key 顺序问题
        ensure_ascii=False,
        separators=(",", ":")    # 去掉多余空格
    )

    return hashlib.md5(text.encode()).hexdigest()


amap_tools = None


async def get_amap_tools():
    global amap_tools

    if amap_tools:
        return amap_tools

    amap_key = os.getenv('AMAP_API_KEY', None)
    if not amap_key:
        raise ValueError('env文件中未配置AMAP_API_KEY，请检查！')
    mcp_info = {
        'amap': {
            'url': f'https://mcp.amap.com/mcp?key={amap_key}',
            'transport': 'http',
            'timeout': 10
        }
    }
    mcp_client = MultiServerMCPClient(mcp_info, tool_interceptors=[limit_amap])

    amap_tools = await mcp_client.get_tools()
    return amap_tools

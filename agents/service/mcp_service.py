import asyncio

from langchain_mcp_adapters.interceptors import MCPToolCallRequest

from utils.logger import log


GLOBAL_AMP_SEM = asyncio.Semaphore(3)


async def limit_amap(request: MCPToolCallRequest, handler):
    tool_name = request.name or ""

    # 只控制高德工具
    if "amap_" in tool_name or "maps_" in tool_name:
        # ⭐执行层限流
        async with GLOBAL_AMP_SEM:
            log.info(f"【limited tools】： {tool_name}")
            result = await handler(request)
            return result
    else:
        log.info(f'【non-limited tools】: {tool_name}')
        return await handler(request)




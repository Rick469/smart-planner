import os

from langchain_mcp_adapters.client import MultiServerMCPClient

from agents.base_agent import BaseAgent
from agents.prompts.planner_prompt import PLANNER_PROMPT
from agents.service.mcp_service import limit_amap


class PlannerAgent(BaseAgent):

    def __init__(self, model_name=None, api_key=None, base_url=None, stream=False):
        super().__init__(model_name, api_key, base_url, stream)

    def get_system_prompt(self) -> str:
        return PLANNER_PROMPT

    def get_user_prompt(self, req: dict):
        request = req.get('request')
        attractions = req.get('attractions')
        weather = req.get('weather')
        hotels = req.get('hotels')

        if not all([request, attractions, weather, hotels]):
            raise ValueError(f'planner-agent参数错误，请检查！')

        return f"""
请根据以下信息生成{request.end_city}{request.start_date}至{request.end_date}的旅行计划:

**基本信息:**
- 城市: {request.end_city}
- 日期: {request.start_date} 至 {request.end_date}
- 酒店偏好: {request.hotel_prefer}
- 景点偏好: {', '.join(request.attraction_prefer) if request.attraction_prefer else '无'}

**景点信息:**
{attractions}

**天气信息:**
{weather}

**酒店信息:**
{hotels}

**要求:**
1. 每天安排2-3个景点
2. 每天必须包含早中晚三餐
3. 每天推荐一个具体的酒店(从酒店信息中选择)
3. 考虑景点之间的距离和交通方式

"""


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





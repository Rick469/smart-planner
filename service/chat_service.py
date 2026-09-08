import json
from models.workflow import WorkflowEvent, WorkflowEventType
from agents.service.agent_service import agent_run, plan
from models.schema import Request, IntentRequest
from models.event import ChatEvent, EventType


class ChatService:


    def __init__(self, agents):

        self.agents = agents


    async def stream_chat(self, request: IntentRequest):

        yield ChatEvent(

            type=EventType.THINKING_START,

            title="识别用户意图"

        )

        intent_result = await agent_run(self.agents.intent_agent, request)

        yield ChatEvent(

            type=EventType.THINKING_END

        )

        if intent_result:
            intent_result = json.loads(intent_result)
        else:
            raise ValueError('意图识别失败！')

        if intent_result.get('intent') == 'greeting':
            # Todo greeting agent
            yield ChatEvent(
                type=EventType.TOKEN,
                content="你好，我是 Smart Planner，您的智能旅行规划助手！"
            )

        elif intent_result.get('intent') == 'travel_plan':

            if intent_result.get('missing_fields'):
                chinese_key_name = {
                    'start_city': '出发城市',
                    'end_city': '到达城市',
                    'start_date': '出发日期',
                    'end_date': '返程日期',
                    'hotel_prefer': '酒店偏好：经济型/舒适型/高档型/豪华型',
                    'attraction_prefer': '景点偏好：自然风光/公园/海滩/历史古迹/人文景观/主题乐园等',
                }
                res = '，'.join([chinese_key_name.get(i) for i in intent_result.get('missing_fields')])
                yield ChatEvent(
                    type=EventType.TOKEN,
                    content='请告诉我其他额外信息：' + res
                )

            elif not intent_result.get('missing_fields') and intent_result.get('fields'):
                req = Request(start_city=intent_result.get('fields').get('start_city', ''),
                              end_city=intent_result.get('fields').get('end_city', ''),
                              start_date=intent_result.get('fields').get('start_date', ''),
                              end_date=intent_result.get('fields').get('end_date', ''),
                              thread_id=request.thread_id)

                agent_list = [self.agents.attraction_agent, self.agents.hotel_agent, self.agents.weather_agent, self.agents.planner_agent]

                async for event in plan(req, *agent_list):

                    if event.type == WorkflowEventType.TOKEN:

                        yield ChatEvent(
                            type=EventType.TOKEN,
                            content=event.content
                        )

                    elif event.type == WorkflowEventType.THINKING_START:

                        yield ChatEvent(
                            type=EventType.THINKING_START,
                            title=event.title
                        )

                    elif event.type == WorkflowEventType.THINKING_END:

                        yield ChatEvent(
                            type=EventType.THINKING_END
                        )

                    elif event.type == WorkflowEventType.TOOL_START:

                        yield ChatEvent(
                            type=EventType.TOOL_START,
                            tool=event.tool,
                            title=event.title
                        )

                    elif event.type == WorkflowEventType.TOOL_END:

                        yield ChatEvent(
                            type=EventType.TOOL_END,
                            tool=event.tool
                        )


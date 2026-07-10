import json
import os
import sys

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from agents.intent_agent import IntentAgent
from agents.service.agent_service import plan, agent_run
from models.schema import Request, IntentRequest
from utils.logger import log

if __name__ == '__main__':
    import time
    import asyncio


    async def main(request: IntentRequest):
        db_url = ''
        if os.getenv('DB_URL'):
            db_url = os.getenv('DB_URL')
        else:
            raise ValueError('DB_URL未配置！')

        async with AsyncPostgresSaver.from_conn_string(db_url) as checkpointer:
            await checkpointer.setup()
            intent_agent = IntentAgent(stream=True, checkpointer=checkpointer)
            intent_result = await agent_run(intent_agent, request)

            if intent_result:
                intent_result = json.loads(intent_result)
            else:
                raise ValueError('意图识别失败！')


            if intent_result.get('intent') == 'greeting':
                # Todo greeting agent
                pass

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
                    return '请告诉我其他额外信息：' + res
                elif not intent_result.get('missing_fields') and intent_result.get('fields'):
                    req = Request(start_city=intent_result.get('fields').get('start_city', ''),
                                  end_city=intent_result.get('fields').get('end_city', ''),
                                  start_date=intent_result.get('fields').get('start_date', ''),
                                  end_date=intent_result.get('fields').get('end_date', ''),
                                  thread_id=request.thread_id)

                    async for content in plan(req, checkpointer):
                        print(content, end='', flush=True)

    before = time.time()

    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )
    request = IntentRequest(thread_id='10', user_input='南京到芜湖，7月5号到7月6号，酒店豪华型，景点海滩或网红打卡点')
    res = asyncio.run(main(request))
    print(111, res)

    after = time.time()
    duration = after - before
    log.info(f'耗时：{duration}秒')

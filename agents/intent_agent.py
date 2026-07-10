from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from agents.base_agent import BaseAgent
from agents.prompts.intent_prompt import INTENT_PROMPT
from models.schema import IntentRequest


class IntentAgent(BaseAgent):

    def get_system_prompt(self) -> str:
        return INTENT_PROMPT

    def get_user_prompt(self, req: IntentRequest) -> str:

        return req.user_input

    async def build_tools(self):
        return None



if __name__ == '__main__':
    import asyncio
    import os

    async def main():
        db_url = ''
        if os.getenv('DB_URL'):
            db_url = os.getenv('DB_URL')
        else:
            raise ValueError('DB_URL未配置！')

        async with AsyncPostgresSaver.from_conn_string(db_url) as checkpointer:
            await checkpointer.setup()
            agent = IntentAgent(stream=True, checkpointer=checkpointer)
            request = IntentRequest(user_input="你是谁？", thread_id="6")
            async for content in agent.run(request):
                print(content, end='', flush=True)

    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )
    asyncio.run(main())

from contextlib import asynccontextmanager
from fastapi import FastAPI
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from utils.logger import log
import os
from service.agent_registry import AgentRegistry


@asynccontextmanager
async def lifespan(app:FastAPI):

    db_url=os.getenv("DB_URL")
    if not db_url:
        raise ValueError('DB_URL未配置！')


    async with AsyncPostgresSaver.from_conn_string(db_url) as checkpointer:

        await checkpointer.setup()


        app.state.agents = AgentRegistry(checkpointer)
        log.info('Agent注册完成...')

        yield


app = FastAPI(

    title="Smart Planner",

    lifespan=lifespan

)



app.include_router(
    chat_router,
    prefix="/api"
)